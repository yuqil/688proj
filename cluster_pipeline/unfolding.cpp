#include <bits/stdc++.h>
#include "unfolding.h"

using namespace std;

double q(double m, int i, int adj_label, double k_i_in, vector<double>& tot, vector<double>& k_i) {
    double ret = k_i_in - 1.0 * tot[adj_label] * k_i[i] / m;
    return ret;
}

double Q(double m, int n, vector<set<int>>& clusters, vector<double>& s_in, vector<double>& tot) {
    double ret = 0;
    for(int i = 0; i < n; i ++) if(clusters[i].size()) {
        ret += s_in[i] / 2.0 / m - (tot[i] / 2.0 / m) * (tot[i] / 2.0 / m);
    }
    return ret;
}

static int depth = 0;

vector<int> fast_unfolding(int n, map<pr, double>& edges) {
    depth ++;
    printf("depth = %d\n", depth);

    // get adjacent list
    vector<vector<int>> adj(n, vector<int>());
    for(auto i = edges.begin(); i != edges.end(); i ++) {
        pr edge = i->first;
        int x = edge.first, y = edge.second;
        if(x != y) {
            adj[x].push_back(y);
            adj[y].push_back(x);
        } else {
            adj[x].push_back(y);
        }
    }

    // bi-edges map
    map<pr, double> biedges;
    for(auto i = edges.begin(); i != edges.end(); i ++) {
        pr edge = i->first;
        int x = edge.first, y = edge.second;
        double weight = i->second;
        biedges[pr(x, y)] = weight;
        biedges[pr(y, x)] = weight;
    }

    // initial label
    vector<int> label(n, 0);
    for(int i = 0; i < n; i ++) label[i] = i;

    // initial clusters
    vector<set<int>> clusters(n, set<int>());
    for(int i = 0; i < n; i ++) clusters[i].insert(i);

    // calculate m
    double m = 0;
    for(auto i = edges.begin(); i != edges.end(); i ++) {
        m += i->second;
    }

    // initial k_i ,s_in andweight
    vector<double> k_i(n, 0);
    vector<double> s_in(n, 0);
    vector<double> w(n, 0);
    for(auto i = edges.begin(); i != edges.end(); i ++) {
        pr edge = i->first;
        int x = edge.first, y = edge.second;
        double weight = i->second;

        k_i[x] += weight;
        k_i[y] += weight;
        if(x == y) {
            w[x] += weight;
            s_in[x] += weight;
        }
    }

    // initial tot
    vector<double> tot(n, 0);
    for(int i = 0; i < n; i ++) {
        tot[i] = k_i[i];
    }

    double Q1 = Q(m, n, clusters,s_in, tot);

    // first pass
    for(int iter = 0; iter < n; iter ++) {
        printf("iters %d\n", iter);
        bool improvement = false;

        // for each node, for each adjacent, calc delta-Q and choose the maximum one
        for(int i = 0; i < n; i ++) {
            int cur_label = label[i];

            double cur_shared_links = 0;
            for(int k = 0; k < adj[i].size(); k ++) {
                int adj_id = adj[i][k];
                int label_k = label[adj[i][k]];
                if(i != adj_id && label_k == cur_label) {
                    cur_shared_links += biedges[pr(i, adj_id)];
                }
            }

            tot[cur_label] -= k_i[i];
            double max_delta_Q = q(m, i, cur_label, cur_shared_links, tot, k_i);
            if(max_delta_Q < 0) max_delta_Q = 0;
            tot[cur_label] += k_i[i];
            
            int max_j = -1;

            set<int> label_cache;
            double best_shared_links;

            for(int j = 0; j < adj[i].size(); j ++) {
                int adj_id = adj[i][j];
                int adj_label = label[adj_id];
                if(adj_label == cur_label) continue;
                if(label_cache.count(adj_label)) continue;
                label_cache.insert(adj_label);
                
                double shared_links = 0;
                for(int k = 0; k < adj[i].size(); k ++) {
                    int adj_id = adj[i][k];
                    int label_k = label[adj_id];
                    if(i != adj_id && label_k == adj_label) {
                        shared_links += biedges[pr(i, adj_id)];
                    }
                }

                double delta_Q = q(m, i, adj_label, shared_links, tot, k_i);
                if(delta_Q > max_delta_Q) {
                    max_j = j;
                    max_delta_Q = delta_Q;
                    best_shared_links = shared_links;
                }
            }

            // change node i's label to node j's label
            if(max_j != -1) {
                int adj_id = adj[i][max_j];
                int adj_label = label[adj_id];

                if(cur_label != adj_label) {
                    improvement = true;
                    label[i] = adj_label;

                    // update tot
                    tot[cur_label] -= k_i[i];
                    tot[adj_label] += k_i[i];

                    // update cluster
                    clusters[cur_label].erase(i);
                    clusters[adj_label].insert(adj_id);

                    // update s_in
                    s_in[cur_label] -= 2 * (cur_shared_links + w[i]);
                    s_in[adj_label] += 2 * (best_shared_links + w[adj_id]);
                }
            }
        }

        if(improvement == false) break;
    }

    double Q2 = Q(m, n, clusters,s_in, tot);
    printf("%f %f\n", Q1, Q2);
    if(depth == 2) return label;

    // second pass
    map<int, int> new_node_map;
    for(int i = 0; i < n; i ++) {
        if(new_node_map.find(label[i]) == new_node_map.end()) {
            int id = new_node_map.size();
            new_node_map[label[i]] = id;
        }
    }
    int new_n = new_node_map.size();
    map<pr, double> new_edges;
    for(auto i = edges.begin(); i != edges.end(); i ++) {
        pr edge = i->first;
        int x = edge.first, y = edge.second;
        x = new_node_map[label[x]];
        y = new_node_map[label[y]];
        double weight = i->second;
        if(x > y) swap(x, y);
        if(new_edges.find(pr(x, y)) == new_edges.end()) {
            if(x == y)
                new_edges[pr(x, y)] = 2 * weight;
            else 
                new_edges[pr(x, y)] = weight;
        } else {
            if(x == y)
                new_edges[pr(x, y)] += 2 * weight;
            else 
                new_edges[pr(x, y)] += weight;
        }
    }
    vector<int> new_label = fast_unfolding(new_n, new_edges);

    // get the final label
    for(int i = 0; i < n; i ++) {
        label[i] = new_label[new_node_map[label[i]]];
    }
    return label;
}


// int main(int argc, char *argv[]) {
//     int n = 6;
//     map<pr, int> test = {{mpr(0,1), 1}, {mpr(1,2), 1}, {mpr(0,2), 1}, {mpr(3,4), 1}, {mpr(2,5), 1}};
//     auto ret = fast_unfolding(n, test, 100);
//     for(int i = 0; i < ret.size(); i ++) printf("%d ", ret[i]);
//     printf("\n");
//     return 0;
// }
