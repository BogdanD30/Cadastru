package ro.cadastru;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import ro.cadastru.config.ConnectionFactory;

public class Main {
    public static void main(String[] args) {
        try (Connection c = ConnectionFactory.getInstance().getConnection();
             Statement s = c.createStatement();
             ResultSet r = s.executeQuery("SELECT count(*) FROM land_use")) {
            r.next();
            System.out.println("land_use rows: " + r.getInt(1));

        } catch (SQLException e) {
            throw new RuntimeException(e);
        }

    }
}