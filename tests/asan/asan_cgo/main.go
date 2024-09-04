package main

// #include <stdlib.h>
//
// int test()
// {
//   int *p = (int *)malloc(10 * sizeof(int));
//   return p[1];
// }
import "C"
import (
	"fmt"
	"strconv"

	"github.com/chyezh/snippets/asan_cgo/asan"
)

func main() {
	dbSizeInfo := make(map[int64]int64)

	for i := 0; i < 1000000; i++ {
		dbSizeInfo[0] += int64(i)
	}
	fmt.Printf("%d", dbSizeInfo[0])

	fmt.Println(int(C.test()))
	asan.LsanDoLeakCheck()
	dbDiskQuotaStr := "3072.0"
	dbDiskQuotaBytes, err := strconv.ParseFloat(dbDiskQuotaStr, 64)
	if err != nil {
		panic(err)
	}
	fmt.Printf("%d", dbDiskQuotaBytes)
	// Output: 42
}
