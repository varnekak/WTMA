<%@ page language="java" %>
<%
    String username = (String) session.getAttribute("username");
%>

<html>
<head>
    <title>Dashboard</title>
</head>
<body>

<h2>Welcome, <%= username %></h2>

<p>You are successfully logged in.</p>

<form action="logout" method="get">
    <input type="submit" value="Logout" />
</form>

</body>
</html>
