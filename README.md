# centro-app

The goal of this app was to use the Central New York Centro Bus API to gather historical data and present bus arrival accuracy. 

These are the files containing the core scripts from a flask app built for my team software development course at SUNY Oswego. I wrote the back-end and implemented the graph.js and javascript in the html that actually displays the historical information (bar graph). I also made some minor edits in the HTML/Inline CSS to improve site responsiveness.  

The back-end gathers data from the SQL database, calculates bus arrival accuracy, and presents that data on the front end. The SQL database used was populated by a Golang script that was not built by our team for time reasons. 
