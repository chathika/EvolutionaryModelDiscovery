package ec.app.myApp;

import org.nlogo.app.App;
public class Main {
  public static void main(String[] argv) {
    App.main(argv);
    try {
      java.awt.EventQueue.invokeAndWait(
    new Runnable() {
      public void run() {
        try {
          App.app().open(
        "models/Sample Models/Earth Science/"
        + "Fire.nlogo");
        }
        catch(java.io.IOException ex) {
          ex.printStackTrace();
        }}});
      App.app().command("set density 62");
      App.app().command("random-seed 0");
      App.app().command("setup");
      App.app().command("repeat 50 [ go ]");
      System.out.println(
    App.app().report("burned-trees"));
    }
    catch(Exception ex) {
      ex.printStackTrace();
    }
  }
}