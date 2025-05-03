#pragma once
#include <vector>
#include <random>
#include <algorithm>
#include <set>

namespace gen_graphs {
    // Tree generator (edges as pairs)
    inline std::vector < std::pair < int, int > > tree (int n, std::mt19937_64 &rng) {
        std::vector < int > nodes(n);
        std::iota(nodes.begin(), nodes.end(), 1);
        std::shuffle(nodes.begin(), nodes.end(), rng);
        std::vector < std::pair < int, int > > edges;
        for (int i = 1; i < n; ++i) {
            int u = nodes[i], v = nodes[std::uniform_int_distribution < int > (0, i - 1)(rng)];
            edges.emplace_back(u, v);
        }
        std::shuffle(edges.begin(), edges.end(), rng);
        return edges;
    }
    // Simple connected graph
    inline std::vector < std::pair < int, int > > simple_graph (int n, int m, std::mt19937_64 &rng) {
        auto edges = tree (n, rng);
        std::set < std::pair < int, int > > edge_set(edges.begin(), edges.end());
        while ((int)edge_set.size() < m) {
            int u = std::uniform_int_distribution < int > (1, n)(rng);
            int v = std::uniform_int_distribution < int > (1, n)(rng);
            if (u != v) edge_set.insert(std::minmax(u, v));
        }
        return std::vector < std::pair < int, int > > (edge_set.begin(), edge_set.end());
    }

    // Generate a random connected weighted graph
    inline std::vector < std::tuple < int, int, int > > weighted_graph (int n, int m, int min_w, int max_w, std::mt19937_64 &rng) {
        auto edges = simple_graph (n, m, rng);
        std::vector < std::tuple < int, int, int > > weighted;
        for (const auto &e : edges) {
            int w = std::uniform_int_distribution < int > (min_w, max_w)(rng);
            weighted.emplace_back(e.first, e.second, w);
        }
        return weighted;
    }

    // Generate a random directed graph (no self-loops, no multi-edges)
    inline std::vector < std::pair < int, int > > directed_graph (int n, int m, std::mt19937_64 &rng) {
        std::set < std::pair < int, int > > edge_set;
        while ((int)edge_set.size() < m) {
            int u = std::uniform_int_distribution < int > (1, n)(rng);
            int v = std::uniform_int_distribution < int > (1, n)(rng);
            if (u != v) edge_set.emplace(u, v);
        }
        return std::vector < std::pair < int, int > > (edge_set.begin(), edge_set.end());
    }

    // Generate a random DAG (Directed Acyclic Graph)
    inline std::vector < std::pair < int, int > > dag (int n, int m, std::mt19937_64 &rng) {
        std::vector < int > nodes(n);
        std::iota(nodes.begin(), nodes.end(), 1);
        std::shuffle(nodes.begin(), nodes.end(), rng);
        std::set < std::pair < int, int > > edge_set;
        while ((int)edge_set.size() < m) {
            int u = std::uniform_int_distribution < int > (0, n - 2)(rng);
            int v = std::uniform_int_distribution < int > (u + 1, n - 1)(rng);
            edge_set.emplace(nodes[u], nodes[v]);
        }
        return std::vector < std::pair < int, int > > (edge_set.begin(), edge_set.end());
    }

    // Generate a random bipartite graph
    inline std::vector < std::pair < int, int > > bipartite (int n1, int n2, int m, std::mt19937_64 &rng) {
        std::set < std::pair < int, int > > edge_set;
        while ((int)edge_set.size() < m) {
            int u = std::uniform_int_distribution < int > (1, n1)(rng);
            int v = std::uniform_int_distribution < int > (1, n2)(rng) + n1;
            edge_set.emplace(u, v);
        }
        return std::vector < std::pair < int, int > > (edge_set.begin(), edge_set.end());
    }

    // Generate a random star graph (center node connected to all others)
    inline std::vector < std::pair < int, int > > star (int n, std::mt19937_64 &rng, int center = 1) {
        std::vector < std::pair < int, int > > edges;
        for (int i = 1; i <= n; ++i) {
            if (i != center) edges.emplace_back(center, i);
        }
        std::shuffle(edges.begin(), edges.end(), rng);
        return edges;
    }

    // Generate a random cycle graph
    inline std::vector < std::pair < int, int > > cycle (int n, std::mt19937_64 &rng) {
        std::vector < int > nodes(n);
        std::iota(nodes.begin(), nodes.end(), 1);
        std::shuffle(nodes.begin(), nodes.end(), rng);
        std::vector < std::pair < int, int > > edges;
        for (int i = 0; i < n; ++i) {
            edges.emplace_back(nodes[i], nodes[(i + 1) % n]);
        }
        return edges;
    }

    // Generate a random complete graph (all pairs)
    inline std::vector < std::pair < int, int > > complete (int n) {
        std::vector < std::pair < int, int > > edges;
        for (int i = 1; i <= n; ++i) {
            for (int j = i + 1; j <= n; ++j) {
                edges.emplace_back(i, j);
            }
        }
        return edges;
    }

    // Generate a random regular graph (each node has degree d)
    inline std::vector < std::pair < int, int > > regular (int n, int d, std::mt19937_64 &rng) {
        if (n * d % 2 != 0 || d >= n) return {};
        std::vector < int > nodes;
        for (int i = 1; i <= n; ++i)
            for (int j = 0; j < d; ++j)
                nodes.push_back(i);
        std::shuffle(nodes.begin(), nodes.end(), rng);
        std::vector < std::pair < int, int > > edges;
        for (size_t i = 0; i < nodes.size(); i += 2) {
            if (nodes[i] == nodes[i + 1]) return {};
            edges.emplace_back(nodes[i], nodes[i + 1]);
        }
        return edges;
    }

    // Generate a random tree with a given diameter
    inline std::vector < std::pair < int, int > > tree_with_diameter (int n, int diameter, std::mt19937_64 &rng) {
        if (diameter >= n) diameter = n - 1;
        std::vector < int > path(diameter + 1);
        std::iota(path.begin(), path.end(), 1);
        std::shuffle(path.begin(), path.end(), rng);
        std::vector < std::pair < int, int > > edges;
        for (int i = 0; i < diameter; ++i) {
            edges.emplace_back(path[i], path[i + 1]);
        }
        int next = diameter + 2;
        while ((int)edges.size() < n - 1) {
            int attach = std::uniform_int_distribution < int > (0, diameter)(rng);
            edges.emplace_back(path[attach], next++);
        }
        std::shuffle(edges.begin(), edges.end(), rng);
        return edges;
    }

    // Generate a chain tree (path tree)
    inline std::vector < std::pair < int, int > > chain_tree (int n) {
        std::vector < std::pair < int, int > > edges;
        for (int i = 2; i <= n; ++i) {
            edges.emplace_back(i - 1, i);
        }
        return edges;
    }
}
