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
    boolean flag=false;
    
    //Constructor starts
    public ConnectionFactory(){
        try{
            Class.forName("com.mysql.jdbc.Driver");
            con=DriverManager.getConnection("jdbc:mysql://localhost/IMS?user=root&password");
            stmt=con.createStatement();
        }catch(Exception e){
            e.printStackTrace();
        }
    }//end of constructor ConnectionFactory
    
    //method Connection starts
    public Connection getConnection(){
        try{
            Class.forName("com.mysql.jdbc.Driver");
            con=DriverManager.getConnection("jdbc:mysql://localhost/IMS?user=root&password");
        }catch(Exception e){
            e.printStackTrace();
        }
        return con;
    }//end of method Connection
    
    //method checkLogin starts
    public boolean checkLogin(String username,String password, String user){
        if(user=="ADMINISTRATOR"){
            String query="SELECT * FROM users WHERE username='"+username+"' AND password='"+password+"' AND category='ADMINISTRATOR'";
            try{
                rs=stmt.executeQuery(query);
                while(rs.next()){
                    flag=true;
                }
            }catch(Exception e){
                e.printStackTrace();
            }
        }else{
            String query="SELECT * FROM users WHERE username='"+username+"' AND password='"+password+"'AND category='NORMAL USER'";
            try{
                rs=stmt.executeQuery(query);
                while(rs.next()){
                    flag=true;
                }
            }catch(Exception e){
                e.printStackTrace();
            }
        }
        return flag;
    }
}
