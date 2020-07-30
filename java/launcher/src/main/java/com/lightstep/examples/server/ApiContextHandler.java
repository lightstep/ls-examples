package com.lightstep.examples.server;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Random;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.eclipse.jetty.servlet.ServletContextHandler;
import org.eclipse.jetty.servlet.ServletHolder;

public class ApiContextHandler extends ServletContextHandler
{
  public ApiContextHandler()
  {
    addServlet(new ServletHolder(new ApiServlet()), "/content");
    addServlet(new ServletHolder(new RandomLengthServlet()), "/getrandomlength");
  }

  static final class RandomLengthServlet extends HttpServlet
  {
    final Random rand = new Random();

    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse res)
      throws ServletException, IOException
    {
      try (PrintWriter writer = res.getWriter()) {
        int retval = rand.nextInt(1023) + 1;
        writer.write(String.valueOf(retval));
      }
    }
  }

  static final class ApiServlet extends HttpServlet
  {
    static final String LETTERS = "abcdefghijklmnopqrstuvwxyz";
    final Random rand = new Random();
    final OkHttpClient client = new OkHttpClient();

    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse res)
      throws ServletException, IOException
    {
      try (PrintWriter writer = res.getWriter()) {
        writer.write(createRandomString(getLengthFromServer()));
      }
    }

    int getLengthFromServer() throws IOException {
      String targetUrl = System.getenv("TARGET_URL");
      if (targetUrl == null || targetUrl.length() == 0)
        targetUrl = "http://127.0.0.1:8083";

      Request clientreq = new Request.Builder()
        .url(targetUrl + "/getrandomlength")
        .build();

      int length = 0;
      try (Response clientres = client.newCall(clientreq).execute()) {
        String body = clientres.body().string();
        length = Integer.valueOf(body);
      }

      return length;
    }

    String createRandomString(int length) {
      StringBuilder sb = new StringBuilder(length);

      for (int i = 0; i < length; i++) {
        sb.append(LETTERS.charAt(rand.nextInt(LETTERS.length())));
      }

      return sb.toString();
    }
  }
}
