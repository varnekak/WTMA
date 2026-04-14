<%@ page language="java" %>
<html>
<head>
    <title>Login</title>
</head>
<body>

<h2>Login</h2>

<form action="login" method="post">
    Username: <input type="text" name="username" required /><br><br>
    Password: <input type="password" name="password" required /><br><br>
    <input type="submit" value="Login" />
</form>

<%
    String error = request.getParameter("error");
    if (error != null) {
%>
<p style="color:red;">Invalid Username or Password</p>
<%
    }
%>

<br>
<a href="signup.jsp">Create New Account</a>

</body>
</html>
