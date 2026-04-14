package com.webtech;

import com.mongodb.client.*;
import javax.servlet.http.*;
import javax.servlet.*;
import javax.servlet.annotation.WebServlet;
import org.bson.Document;

import java.io.IOException;

@WebServlet("/login")
public class Login extends HttpServlet {

    private MongoCollection<Document> userCollection;

    @Override
    public void init() {
        MongoClient client = MongoClients.create("mongodb://localhost:27017");
        MongoDatabase db = client.getDatabase("servlet_lab");
        userCollection = db.getCollection("users");
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String username = request.getParameter("username");
        String password = request.getParameter("password");

        Document user = userCollection.find(
                new Document("username", username)
                        .append("password", password)
        ).first();

        if (user != null) {
            HttpSession session = request.getSession(true);
            session.setAttribute("username", username);
            session.setMaxInactiveInterval(300); // 5 minutes

            response.sendRedirect("dashboard");
        } else {
            response.sendRedirect("index.jsp?error=1");
        }
    }
}
