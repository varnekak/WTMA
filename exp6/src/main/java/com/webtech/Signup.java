package com.webtech;

import com.mongodb.client.*;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import org.bson.Document;

import java.io.IOException;

@WebServlet("/signup")
public class Signup extends HttpServlet {

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

        Document existingUser = userCollection.find(
                new Document("username", username)
        ).first();

        if (existingUser != null) {
            response.sendRedirect("signup.jsp?msg=exists");
            return;
        }

        Document newUser = new Document("username", username)
                .append("password", password);

        userCollection.insertOne(newUser);

        response.sendRedirect("signup.jsp?msg=success");
    }
}
