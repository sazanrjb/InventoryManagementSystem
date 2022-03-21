package com.inventory.dao;

import java.sql.ResultSet;
import java.sql.Statement;

public class Stocks {
    boolean flag=false;
    public boolean checkStock(String productcode, Statement stmt){
        try{
            String query="SELECT * FROM currentstocks where productcode='"+productcode+"'";
            ResultSet rs=stmt.executeQuery(query);
            while(rs.next()){
                flag=true;
            }
        }catch(Exception e){
            e.printStackTrace();
        }
        return flag;
    }

}
