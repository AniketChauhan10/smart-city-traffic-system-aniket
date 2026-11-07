## &#x20;Smart City Traffic Management and Route Optimization System



### Project Overview



The Smart City Traffic Management System is a Python-based project that uses graph algorithms to model road networks, find efficient routes, analyze traffic congestion, explore network connectivity, and optimize infrastructure planning.



The city road network is represented as a weighted graph:

\- Vertices represent intersections.

\- Edges represent roads.

\- Weights represent travel costs.



### Features



\- \*\*Road Network Modeling:\*\* Graph visualization, adjacency list, and adjacency matrix.

\- \*\*Route Planning:\*\* Finds shortest routes using Dijkstra's Algorithm.

\- \*\*Traffic Analysis:\*\* Simulates congestion and compares routes using Bellman-Ford Algorithm.

\- \*\*Network Connectivity:\*\* Explores intersections using BFS and DFS.

\- \*\*Infrastructure Planning:\*\* Generates Minimum Spanning Trees using Prim's and Kruskal's Algorithms.

\- \*\*Performance Analysis:\*\* Compares algorithm execution times on networks of 10, 25, 50, and 100 intersections.

\- \*\*Interactive Dashboard:\*\* Displays results through a Streamlit application.



### Algorithms Implemented

| Algorithm | Purpose |

|---|---|

| Dijkstra | Shortest path |

| Bellman-Ford | Shortest path and traffic analysis |

| BFS | Breadth-first graph traversal |

| DFS | Depth-first graph traversal |

| Prim | Minimum Spanning Tree |

| Kruskal | Minimum Spanning Tree |



### Technologies Used



\- Python

\- Streamlit

\- NetworkX

\- Matplotlib

\- Pandas

\- NumPy

\- Jupyter Notebook



### Project Structure



smart-city-traffic-system/

│

├── app.py

├── route\_planner.py

├── traffic\_analysis.py

├── connectivity\_module.py

├── mst\_planner.py

├── capstone.ipynb

├── requirements.txt

├── README.md

│

├── screenshots/

│   ├── 01\_city\_network.png

│   ├── 02\_route\_planning.png

│   ├── 03\_traffic\_analysis.png

│   ├── 04\_network\_connectivity.png

│   └── 05\_infrastructure\_planning.png

│

└── Final\_Project\_Report.pdf



### Installation and Setup



1\. Clone the repository





git clone <https://github.com/AniketChauhan10>



2\. Navigate to the project folder



cd smart-city-traffic-system



3\. Create a virtual environment



python -m venv venv



4\. Activate the environment



Windows:



venv\\Scripts\\activate



5\. Install dependencies



pip install -r requirements.txt



### Run the Application



Start the Streamlit application using:



streamlit run app.py



### Sample Results



The sample city network contains six intersections (A–F).



\- Original shortest route cost: 13

\- Updated route cost after congestion: 14

\- Prim's and Kruskal's algorithms produce an MST with total cost 13.



### Performance Analysis



The project evaluates six graph algorithms across networks of different sizes and compares their execution times.



The experiments demonstrate the performance differences between traversal, shortest-path, and minimum-spanning-tree algorithms.



### Future Improvements



\- Integration of real-time traffic data.

\- Dynamic road closure detection.

\- Real-world city map integration.

\- Intelligent traffic signal optimization.

\- Machine learning-based traffic prediction.





Design and Analysis of Algorithms Lab (ENCA351)



