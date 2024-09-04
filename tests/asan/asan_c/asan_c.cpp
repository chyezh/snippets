#include <iostream>
#include <memory>
#include <stdio.h>
#include <stdlib.h>
#include <string_view>
#include <unordered_map>
#include <variant>

using Metrics =
    std::variant<int8_t, int16_t, int32_t, int64_t, float, double, std::string>;

// MetricsDataType is used to avoid copy when get min/max value fro
// FieldChunkMetrics
template <typename T>
using MetricsDataType =
    std::conditional_t<std::is_same_v<T, std::string_view>, std::string, T>;

struct FieldChunkMetrics {
  Metrics min_;
  Metrics max_;
  bool hasValue_;
  int64_t null_count_;

  FieldChunkMetrics() : hasValue_(false){};

  template <typename T> std::pair<T, T> GetMinMax() const {
    T lower_bound;
    T upper_bound;
    try {
      lower_bound = std::get<MetricsDataType<T>>(min_);
      upper_bound = std::get<MetricsDataType<T>>(max_);
    } catch (const std::bad_variant_access &e) {
      return {};
    }
    return {lower_bound, upper_bound};
  }
};

int main(int argc, char *argv[]) {
  auto s = std::string("12312231");
  Metrics m1 = Metrics(std::move(s));
  s = std::string("123122312");
  Metrics m2 = Metrics(std::move(s));

  FieldChunkMetrics fcm;
  fcm.min_ = m1;
  fcm.max_ = m2;

  auto [min, max] = fcm.GetMinMax<std::string_view>();
  std::cout << min << " " << max << std::endl;
  return 0;
}
