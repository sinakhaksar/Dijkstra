import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for _ in range(vertices)] for _ in range(vertices)]

    def print_solution(self, dist, parent, dest, src):
        path = self.print_path(parent, dest, [])
        path = list(map(lambda x: chr(ord('A') + x), path))
        print(f"Shortest Path from {chr(ord('A') + src)} to {chr(ord('A') + dest)}:")
        print(" -> ".join(path))
        print("The weight is:", dist[dest])
        return path  # Return the path for visualization

    def print_path(self, parent, j, path):
        if parent[j] == -1:
            path.append(j)
            return path
        path = self.print_path(parent, parent[j], path)
        path.append(j)
        return path

    def min_distance(self, dist, spt_set):
        min_val = float('inf')
        min_index = -1
        for v in range(self.V):
            if dist[v] < min_val and not spt_set[v]:
                min_val = dist[v]
                min_index = v
        return min_index

    def dijkstra(self, src, dest):
        src, dest = self.get_node_indices(src, dest)

        dist = [float('inf')] * self.V
        parent = [-1] * self.V
        dist[src] = 0
        spt_set = [False] * self.V

        for _ in range(self.V):
            u = self.min_distance(dist, spt_set)
            if u == -1:  # No valid vertex found
                break
            spt_set[u] = True

            for v in range(self.V):
                if self.graph[u][v] > 0 and not spt_set[v] and dist[v] > dist[u] + self.graph[u][v]:
                    dist[v] = dist[u] + self.graph[u][v]
                    parent[v] = u

        return self.print_solution(dist, parent, dest, src)

    def visualize_graph(self, path, seed=None):
        G = nx.Graph()  

        for u in range(self.V):
            G.add_node(u, label=chr(ord('A') + u))

        for u in range(self.V):
            for v in range(self.V):
                if self.graph[u][v] > 0:
                    G.add_edge(u, v, weight=self.graph[u][v])

        pos = nx.spring_layout(G, seed=seed)
        labels = nx.get_edge_attributes(G, 'weight')
        node_labels = nx.get_node_attributes(G, 'label')

        edge_colors = []
        for edge in G.edges():
            if (chr(ord('A') + edge[0]) in path and chr(ord('A') + edge[1]) in path and
                abs(path.index(chr(ord('A') + edge[0])) - path.index(chr(ord('A') + edge[1]))) == 1):
                edge_colors.append('red')
            else:
                edge_colors.append('black')

        nx.draw(G, pos, with_labels=True, labels=node_labels, edge_color=edge_colors, node_color='lightblue',)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.show()

    def get_node_indices(self, src, dest):
        try:
            src_index = int(src)
        except ValueError:
            src_index = ord(src.upper()) - ord('A')

        try:
            dest_index = int(dest)
        except ValueError:
            dest_index = ord(dest.upper()) - ord('A')

        return src_index, dest_index

    def show_options(self):
        print("Available nodes:")
        for u in range(self.V):
            print(f"{u}: {chr(ord('A') + u)}")



def main():
    g = Graph(9)
    g.graph = [
        [0, 4, 0, 0, 0, 0, 0, 8, 0],
        [4, 0, 8, 0, 0, 0, 0, 11, 0],
        [0, 8, 0, 7, 0, 4, 0, 0, 2],
        [0, 0, 7, 0, 9, 14, 0, 0, 0],
        [0, 0, 0, 9, 0, 10, 0, 0, 0],
        [0, 0, 4, 14, 10, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 1, 6],
        [8, 11, 0, 0, 0, 0, 1, 0, 7],
        [0, 0, 2, 0, 0, 0, 6, 7, 0]
    ]

    g.show_options()
    
    src_node = input("Enter the source node (A - I): ").upper()
    dest_node = input("Enter the destination node (A - I): ").upper()

    # Validate input nodes
    valid_values = "ABCDEFGHI"

    if src_node not in valid_values or dest_node not in valid_values:
        print("Invalid input. Please enter nodes between A and I.")
        return

    path = g.dijkstra(src_node, dest_node)
    g.visualize_graph(path, seed=19)


if __name__ == "__main__":
    main()
