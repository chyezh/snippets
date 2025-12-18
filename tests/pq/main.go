package main

import (
	"context"
	"fmt"

	clientv3 "go.etcd.io/etcd/client/v3"
)

func main() {
	client, err := clientv3.New(clientv3.Config{Endpoints: []string{"localhost:2379"}})
	if err != nil {
		panic(err)
	}
	defer client.Close()

	ctx := context.Background()

	client.Put(ctx, "test3", "test")

	resp, err := client.Get(ctx, "test")
	fmt.Println(resp)

	resp, err = client.Get(ctx, "test2")
	fmt.Println(resp)
	fmt.Println(err)

	lease, err := client.Grant(ctx, 10)
	if err != nil {
		panic(err)
	}

	resp3, err := client.Txn(ctx).If(
		clientv3.Compare(clientv3.Version("test4"), "=", 0),
		clientv3.Compare(clientv3.ModRevision("test"), "=", 2),
	).Then(clientv3.OpPut("test6", "test"), clientv3.OpPut("test7", "test", clientv3.WithLease(lease.ID))).Commit()
	fmt.Println(resp3)
	fmt.Println(err)
}
