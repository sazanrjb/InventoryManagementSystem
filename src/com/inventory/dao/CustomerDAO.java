/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package com.inventory.dao;

import com.inventory.database.ConnectionFactory;
import com.inventory.dto.CustomerDTO;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Vector;
import javax.swing.JOptionPane;
import javax.swing.table.DefaultTableModel;

/**
 *
 * @author ADMIN
 */
public class CustomerDAO {
    Connection con = null;
    PreparedStatement pstmt = null;
    Statement stmt = null;
    ResultSet rs = null;
    
    public CustomerDAO(){
        try {
            con = new ConnectionFactory().getConnection();
            stmt = con.createStatement();
        } catch (Exception e) {
                e.printStackTrace();
        }
    }
    
     public void addCustomerDAO(CustomerDTO customerdto) {
        try{
            /***
             * Refactoring name: RENAME VARIABLE - 1
             * Changed names of variables to give it a meaningful name
             */
            String findCustomersByNameLocationAndPhone = "SELECT * FROM customers WHERE fullname='"+customerdto.getFullName()+"' AND location='"+customerdto.getLocation()+"' AND phone='"+customerdto.getPhone()+"'";
                rs=stmt.executeQuery(findCustomersByNameLocationAndPhone);
                if(rs.next()){
                    JOptionPane.showMessageDialog(null,"Same Customer has already been added!");
                }else{
                    addFunction(customerdto);
                }
        }catch(Exception e){
                e.printStackTrace();
        }           
    }//end of method addCustomerDTO
     
     public void addFunction(CustomerDTO customerdto){
         try {
                        String customerCode = null;
                        String oldCustomerCode = null;

             /***
              * Refactoring name: RENAME VARIABLE - 2
              * Changed names of variables to give it a meaningful name
              */
             String getAllCustomers="SELECT * FROM customers";
                        rs=stmt.executeQuery(getAllCustomers);
                        if(!rs.next()){
                            customerCode="cus"+"1"; 
                        }
                        else{
                            /***
                             * Refactoring name: RENAME VARIABLE - 3
                             * Changed names of variables to give it a meaningful name
                             */
                            String getAllCustomersInDescOrder="SELECT * FROM customers ORDER by cid DESC";
                            rs=stmt.executeQuery(getAllCustomersInDescOrder);
                            if(rs.next()){
                                oldCustomerCode=rs.getString("customercode");
                                Integer scode=Integer.parseInt(oldCustomerCode.substring(3));
                                scode++;    
                                customerCode="cus"+scode;
                            }
                        }

             /***
              * Refactoring name: RENAME VARIABLE - 4
              * Changed names of variables to give it a meaningful name
              */
             String insertCustomers = "INSERT INTO customers VALUES(null,?,?,?,?)";
                            pstmt = (PreparedStatement) con.prepareStatement(insertCustomers);
                            pstmt.setString(1, customerCode);
                            pstmt.setString(2, customerdto.getFullName());
                            pstmt.setString(3, customerdto.getLocation());
                            pstmt.setString(4, customerdto.getPhone());
                            pstmt.executeUpdate();
                            JOptionPane.showMessageDialog(null, "Inserted Successfully");
                        }catch (Exception e) {
                            e.printStackTrace();
                        }
     }
     
    public void editCustomerDAO(CustomerDTO customerdto){
          try {
              /***
               * Refactoring name: RENAME VARIABLE - 5
               * Changed names of variables to give it a meaningful name
               */
                String updateCustomerDetails = "UPDATE customers SET fullname=?,location=?,phone=? WHERE customercode=?";
                pstmt = (PreparedStatement) con.prepareStatement(updateCustomerDetails);
                pstmt.setString(1, customerdto.getFullName());
                pstmt.setString(2, customerdto.getLocation());
                pstmt.setString(3, customerdto.getPhone());
                pstmt.setString(4, customerdto.getCustomerCode());
                pstmt.executeUpdate();
                JOptionPane.showMessageDialog(null, "Updated Successfully!");
                    
            } catch (Exception e) {
                e.printStackTrace();
            } 
    }
    
    public void deleteCustomerDAO(String value){
        try{
            System.out.println(value);
            /***
             * Refactoring name: RENAME VARIABLE - 6
             * Changed names of variables to give it a meaningful name
             */
            String deleteCustomerByCode="delete from customers where customercode=?";
            pstmt=con.prepareStatement(deleteCustomerByCode);
            pstmt.setString(1,value);
            pstmt.executeUpdate();
            JOptionPane.showMessageDialog(null, "Deleted..");
        }catch(SQLException  e){
            e.printStackTrace();
        }
    }


    public ResultSet getQueryResult() {
        try {
            /***
             * Refactoring name: RENAME VARIABLE - 7
             * Changed names of variables to give it a meaningful name
             */
            String getCustomersDetails = "SELECT customercode AS CustomerCode, fullname AS Name, location AS Location, phone AS Phone FROM customers";
            rs = stmt.executeQuery(getCustomersDetails);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return rs;
    }//end of method getQueryResult
    
    public ResultSet getCreditCustomersQueryResult() {
        try {
            /***
             * Refactoring name: RENAME VARIABLE - 8
             * Changed names of variables to give it a meaningful name
             */
            String getCustomersWithCredit = "SELECT * FROM customers WHERE credit>0";
            rs = stmt.executeQuery(getCustomersWithCredit);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return rs;
    }
    
    public ResultSet getDebitCustomersQueryResult() {
        try {
            /***
             * Refactoring name: RENAME VARIABLE - 9
             * Changed names of variables to give it a meaningful name
             */
            String getCustomersWithDebit = "SELECT * FROM customers WHERE credit=0";
            rs = stmt.executeQuery(getCustomersWithDebit);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return rs;
    }
    
    public ResultSet getSearchCustomersQueryResult(String searchTxt) {
        try {
            /***
             * Refactoring name: RENAME VARIABLE - 10
             * Changed names of variables to give it a meaningful name
             */
            String getCustomers = "SELECT * FROM customers WHERE fullname LIKE '%"+searchTxt+"%' OR location LIKE '%"+searchTxt+"%' OR customercode LIKE '%"+searchTxt+"%' OR phone LIKE '%"+searchTxt+"%'";
            rs = stmt.executeQuery(getCustomers);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return rs;
    }
    
    public ResultSet getCustomersName(String customerCode){
        try{
            /***
             * Refactoring name: RENAME VARIABLE - 11
             * Changed names of variables to give it a meaningful name
             */
            String getCustomersByCode="SELECT * FROM customers WHERE customercode='"+customerCode+"'";
            rs=stmt.executeQuery(getCustomersByCode);
        }catch(Exception e){
            e.printStackTrace();
        }
        return rs;
    }
    
    public ResultSet getProductsName(String productCode){
        try{
            /***
             * Refactoring name: RENAME VARIABLE - 12
             * Changed names of variables to give it a meaningful name
             */
            String getCustomersByProductCode="SELECT productname, currentstocks.quantity FROM products INNER JOIN currentstocks ON products.productcode=currentstocks.productcode WHERE currentstocks.productcode='"+productCode+"'";
            rs=stmt.executeQuery(getCustomersByProductCode);
        }catch(Exception e){
            e.printStackTrace();
        }
        return rs;
    }

    //start of method DefaultTableModel
    public DefaultTableModel buildTableModel(ResultSet rs) throws SQLException {
        ResultSetMetaData metaData = rs.getMetaData(); //resultset ko metadata
        Vector<String> columnNames = new Vector<String>();
        int columnCount = metaData.getColumnCount();

        for (int column = 1; column <= columnCount; column++) {
            columnNames.add(metaData.getColumnName(column));
        }

        Vector<Vector<Object>> data = new Vector<Vector<Object>>();
        while (rs.next()) {
            Vector<Object> vector = new Vector<Object>();
            for (int columnIndex = 1; columnIndex <= columnCount; columnIndex++) {
                vector.add(rs.getObject(columnIndex));
            }
            data.add(vector);
        }
        return new DefaultTableModel(data, columnNames);
    }//end of method DefaultTableModel
}
