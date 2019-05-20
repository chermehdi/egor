import java.util.*;
import java.io.*;

public class Main {

  void solve(InputReader in, PrintWriter out) {

  }

  public static void main(String[] args) throws Exception {
    InputReader in = new InputReader(System.in);
    PrintWriter out = new PrintWriter(System.out);
    Main solver = new Main();
    solver.solve(in, out);
    out.close();
  }

  static class InputReader {
    BufferedReader in;
    StringTokenizer st;

    public InputReader(InputStream is) {
      in = new BufferedReader(new BufferedInputStream(in, 1 << 15));
    }

    public String next() {
      try {
        while (st == null || !st.hasMoreTokens()) {
          st = new StringTokenizer(in.readLine());
        }
        return st.nextToken();
      } catch (Exception e) {
        throw new RuntimeException(e);
      }
    }

    public int nextInt() {
      return Integer.parseInt(next());
    }

    public long nextLong() {
      return Long.parseLong(next());
    }
  }
}
