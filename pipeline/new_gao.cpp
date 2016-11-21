#include <bits/stdc++.h>

using namespace std;
#define MAXN 1000

int n; // number of people
int m; // number of edge
map<string, string> person; // id to person name
vector<pair<int, int>> edges; // all edge
set<pair<int, int>> edges_map; // eliminate duplicate
vector<vector<int>> edge; // adjacent list

map<int, string> i2id;
map<string, int> id2i; // map of id

bool open_finder = false;

bool parse(string &id, string &name, char *s) {
    int comma = 0;
    for(int i = 0 ; i < strlen(s); i ++) if(s[i] == ',') {comma = i; break;}
    if(comma == 0 || comma >= strlen(s) - 1) return false;
    s[comma] = 0;
    id = string(s);
    name = string(s + comma + 1);
    return true;
}

void readPerson(char *person_file) {
    fprintf(stderr, "reading person file...\n");
    ifstream pfile(person_file);
    assert(pfile.good());

    char buf[MAXN];
    string id;
    string name;
    int ignore = 0;
    int cnt = 0;
    
    while(pfile.getline(buf, MAXN)) {
        if(!parse(id, name, buf)) {
            ignore ++;
            continue;
        }
        assert(person.find(id) == person.end()); // id never appear
        person[id] = name;
        cnt ++;
    }

    if(ignore) fprintf(stderr, "[warn] ignored %d line of person file\n", ignore);
    pfile.close();
}

int geti(string id) {
    if(id2i.find(id) == id2i.end()) {
        int i = id2i.size();
        id2i[id] = i;
        i2id[i] = id;
    }
    return id2i[id];
}

void readEdge(char *edge_file) {
    fprintf(stderr, "reading edge file...\n");
    ifstream efile(edge_file);
    assert(efile.good());

    string id1, id2;
    int ignore = 0;
    
    while(efile >> id1 >> id2) {
        if(person.find(id1) == person.end() ||
           person.find(id2) == person.end()) {
            ignore ++;
            continue;
        }
        int i1 = geti(id1), i2 = geti(id2);
        if(i1 > i2) swap(i1, i2);
        if(edges_map.count(make_pair(i1, i2))) {
            fprintf(stderr, "[warn] ignored duplicates %d %d\n", i1, i2);
            ignore ++;
            continue;
        }

        edges.push_back(make_pair(i1, i2));
        edges_map.insert(make_pair(i1, i2));
    }

    if(ignore) fprintf(stderr, "[warn] ignored %d line of edge file\n", ignore);

    n = id2i.size();
    m = edges.size();
}

vector<int> update(vector<int> &label) {
    vector<int> ret;
    
    // for each node, find the maximum count of label of adjacency
    for(int i = 0; i < n; i ++) {
        map<int, int> count;
        int chosen_label = -1;
        int max_cnt = 0;
        int same_max_cnt = 0;
        for(int j = 0; j < edge[i].size(); j ++) {
            int adj_label = label[edge[i][j]];
            count[adj_label] ++;
            int adj_label_cnt = count[adj_label];
            
            // find the maximum one
            if(adj_label_cnt > max_cnt) {
                max_cnt = adj_label_cnt;
                chosen_label = adj_label;
                same_max_cnt = 1;
            } else if(adj_label_cnt == max_cnt) {
                same_max_cnt ++;
                if(rand() % same_max_cnt == 0) {
                    chosen_label = adj_label;
                }
            }
        }
        ret.push_back(chosen_label);
    }

    return ret;
}


void solve(char *person_file, char *edge_file, int iters) {
    readPerson(person_file);
    readEdge(edge_file);
    
    fprintf(stderr, "[info] node number %d\n[info] edge number %d\n", n, m);

    // parse edge
    edge.resize(m, vector<int>()); // adjacent list
    for(int i = 0; i < m; i ++) {
        int x = edges[i].first;
        int y = edges[i].second;
        edge[x].push_back(y);
        edge[y].push_back(x);
    }

    // initialize label
    vector<int> label(n);
    for(int i = 0; i < n; i ++) label[i] = i;
    
    for(int iter = 0; iter < iters; iter ++) {
        if(iter % 10 == 0)
            fprintf(stderr, "[info] iter %d / %d\n", iter, iters);
        vector<int> new_label = update(label);
        label = new_label;
    }

    // rename cluster id
    map<int, int> p2id;
    for(int i = 0; i < n; i ++) {
        if(p2id.find(label[i]) == p2id.end()) {
            int val = p2id.size();
            p2id[label[i]] = val;
        }
        label[i] = p2id[label[i]];
    }

    // get clusters
    int cluster_size = p2id.size();
    vector<vector<int>> clusters(cluster_size, vector<int>());
    for(int i = 0; i < n; i ++) {
        clusters[label[i]].push_back(i);
    }

    // output
    ofstream outputs("output.txt");
    for(int i = 0; i < cluster_size; i ++) {
        outputs << "Cluster " << i << ":\n";
        for(int j = 0; j < clusters[i].size(); j ++) {
            outputs << person[i2id[clusters[i][j]]] << "\n";
        }
        outputs << "\n";
    }
    outputs.close();

    fprintf(stderr, "[info] finished\n");
    fprintf(stderr, "[info] cluster size %d\n", cluster_size);
    fprintf(stderr, "[info] output file: output.txt\n");

    if(!open_finder) return ;

    // finder
    map<string, vector<string>> finder;
    for(auto i = person.begin(); i != person.end(); i ++) {
        finder[i->second].push_back(i->first);
    }
    char buf[MAXN];
    while(cin.getline(buf, MAXN)) {
        string name = string(buf);
        if(finder.find(name) == finder.end()) {
            fprintf(stdout, "Not Found\n");
            continue;
        }
        auto &v = finder[name];
        for(int i = 0; i < v.size(); i ++) {
            string nid = v[i];
            int id = id2i[nid];
            fprintf(stdout, "cluster: %d\n", label[id]);
        }
    }
}


int main(int argc, char *argv[]) {
    if(argc < 4) {
        fprintf(stderr, "Usage: %s [person_file] [edge_file] [iteration] [open finder]\n\n", argv[0]);
        return 0;
    }
    srand((unsigned)time(NULL));
    if(argc > 4) open_finder = atoi(argv[4]);
    solve(argv[1], argv[2], atoi(argv[3]));
    return 0;
}