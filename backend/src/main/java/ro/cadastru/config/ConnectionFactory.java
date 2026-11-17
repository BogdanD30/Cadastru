package ro.cadastru.config;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class ConnectionFactory {
    private  final String user;
    private final String pass;
    private final String url;
    private ConnectionFactory(){
            this.user = System.getenv("POSTGRES_USER");
            this.pass = System.getenv("POSTGRES_PASSWORD");
            this.url = "jdbc:postgresql://localhost:5432/"+System.getenv("POSTGRES_DB");

    }
    private static class Holder{
        private static final ConnectionFactory INSTANCE = new ConnectionFactory();
    }

    public static ConnectionFactory getInstance(){
            return Holder.INSTANCE;
    }

    public Connection getConnection() throws SQLException{
        return DriverManager.getConnection(url,user,pass);
    }
}
