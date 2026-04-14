<%@ page language="java" %>
<html>
<head>
  <title>Create Account</title>
</head>
<body>

<h2>Create Account</h2>

<form action="signup" method="post">
  Username: <input type="text" name="username" required /><br><br>
  Password: <input type="password" name="password" required /><br><br>
  <input type="submit" value="Create Account" />
</form>

<%
  String msg = request.getParameter("msg");
  if ("exists".equals(msg)) {
%>
<p style="color:red;">Username already exists</p>
<%
} else if ("success".equals(msg)) {
%>
<p style="color:green;">Account created successfully</p>
<%
  }
%>

<br>
<a href="index.jsp">Go back to Login</a>

</body>
</html>
