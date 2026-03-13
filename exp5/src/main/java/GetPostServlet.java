

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class GetPostServlet
 */
@WebServlet("/GetPostServlet")
public class GetPostServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public GetPostServlet() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
    protected void doGet(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {

        response.setContentType("text/html");

        String name = request.getParameter("name");
        String email = request.getParameter("email");

        response.getWriter().println("<html><body>");
        response.getWriter().println("<h2>GET Method Used</h2>");
        response.getWriter().println("Name: " + name + "<br>");
        response.getWriter().println("Email: " + email + "<br>");
        response.getWriter().println("<p>Data is visible in URL.</p>");
        response.getWriter().println("</body></html>");
    }
	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
    protected void doPost(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {

        response.setContentType("text/html");

        String name = request.getParameter("name");
        String email = request.getParameter("email");

        response.getWriter().println("<html><body>");
        response.getWriter().println("<h2>POST Method Used</h2>");
        response.getWriter().println("Name: " + name + "<br>");
        response.getWriter().println("Email: " + email + "<br>");
        response.getWriter().println("<p>Data is NOT visible in URL.</p>");
        response.getWriter().println("</body></html>");
    }

}
