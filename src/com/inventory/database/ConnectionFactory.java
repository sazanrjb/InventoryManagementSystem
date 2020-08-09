/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.inventory.database;

import java.sql.Statement;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;

/**
 *
 * @author ADMIN
 */
public class ConnectionFactory {

    Connection con = null;
    Statement stmt = null;
    ResultSet rs = null;
    
    public ConnectionFactory(){
        try{
            Class.forName("com.mysql.jdbc.Driver");
            con=DriverManager.getConnection("jdbc:mysql://localhost/ims?user=root&password=root");
            stmt=con.createStatement();
        }catch(Exception e){
            e.printStackTrace();
        }
    }
    
    public Connection getConnection(){
        try{
            Class.forName("com.mysql.jdbc.Driver");
            con=DriverManager.getConnection("jdbc:mysql://localhost/ims?user=root&password=root");
        }catch(Exception e){
            e.printStackTrace();
        }
        return con;
    }

    public boolean checkLogin(String username,String password, String user){
        String query="SELECT * FROM users WHERE username='"+username+"' AND password='"+password+"' AND category='ADMINISTRATOR' LIMIT 1";
        try{
            rs=stmt.executeQuery(query);
            if(rs.next()){
                return true;
            }
        }catch(Exception e){
            e.printStackTrace();
        }
            
        return false;
    }
}
