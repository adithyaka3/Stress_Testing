#pragma once
#include <random>
#include <limits>
#include <set>
#include <vector>

namespace gen_numbers {
    template < typename T = long long >
    T random (T l, T r, std::mt19937_64 &rng) {
        return std::uniform_int_distribution < T > (l, r)(rng);
    }

    template < typename T = long long >
    std::vector < T > random_range (T l, T r, int count, std::mt19937_64 &rng) {
        std::vector < T > v(count);
        for (auto &x : v) x = random < T > (l, r, rng);
        return v;
    }

    // Generate a random number with exclusion set
    template < typename T = long long >
    T random_exclude (T l, T r, const std::set < T > &exclude, std::mt19937_64 &rng) {
        T val;
        do {
            val = random < T > (l, r, rng);
        } while (exclude.count(val));
        return val;
    }

    // Generate a vector of random numbers with exclusion set
    template < typename T = long long >
    std::vector < T > random_range_exclude (T l, T r, int count, const std::set < T > &exclude, std::mt19937_64 &rng) {
        std::vector < T > v;
        while ((int)v.size() < count) {
            T val = random < T > (l, r, rng);
            if (!exclude.count(val)) v.push_back(val);
        }
        return v;
    }

    // Generate a random number with a custom probability distribution
    template < typename T = long long >
    T random_weighted (const std::vector < T > &values, const std::vector < double > &weights, std::mt19937_64 &rng) {
        std::discrete_distribution <> dist(weights.begin(), weights.end());
        return values[dist(rng)];
    }

    // Flexible: random floating point
    template < typename T = double >
    T random_real (T l, T r, std::mt19937_64 &rng) {
        return std::uniform_real_distribution < T > (l, r)(rng);
    }

    // Generate a random floating point number with exclusion interval
    template < typename T = double >
    T random_real_exclude (T l, T r, T excl_l, T excl_r, std::mt19937_64 &rng) {
        T val;
        do {
            val = random_real < T > (l, r, rng);
        } while (val >= excl_l && val <= excl_r);
        return val;
    }
}
