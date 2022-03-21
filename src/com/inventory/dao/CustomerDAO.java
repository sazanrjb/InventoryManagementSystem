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

    /***
     * Refactoring name: RENAME VARIABLE
     * Changed variable name from query => findCustomersByNameLocationAndPhone
     */
     public void addCustomerDAO(CustomerDTO customerdto) {
        try{
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

    /***
     * Refactoring name: RENAME VARIABLE
     * Changed variable name from
     * query1 => getAllCustomers
     * query2 => getAllCustomersInDescOrder
     * q => insertCustomers
     */
     public void addFunction(CustomerDTO customerdto){
         try {
                        String customerCode = null;
                        String oldCustomerCode = null;
                        String getAllCustomers="SELECT * FROM customers";
                        rs=stmt.executeQuery(getAllCustomers);
                        if(!rs.next()){
                            customerCode="cus"+"1"; 
                        }
                        else{
                            String getAllCustomersInDescOrder="SELECT * FROM customers ORDER by cid DESC";
                            rs=stmt.executeQuery(getAllCustomersInDescOrder);
                            if(rs.next()){
                                oldCustomerCode=rs.getString("customercode");
                                Integer scode=Integer.parseInt(oldCustomerCode.substring(3));
                                scode++;    
                                customerCode="cus"+scode;
                            }
                        }
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

    /***
     * Refactoring name: RENAME VARIABLE
     * Changed variable name from query => updateCustomerDetails
     */
    public void editCustomerDAO(CustomerDTO customerdto){
          try {
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

    /***
     * Refactoring name: RENAME VARIABLE
     * Changed variable name from query => deleteCustomerByCode
     */
    public void deleteCustomerDAO(String value){
        try{
            System.out.println(value);
            String deleteCustomerByCode="delete from customers where customercode=?";
            pstmt=con.prepareStatement(deleteCustomerByCode);
            pstmt.setString(1,value);
            pstmt.executeUpdate();
            JOptionPane.showMessageDialog(null, "Deleted..");
        }catch(SQLException  e){
            e.printStackTrace();
        }
    }


    /***
     * Refactoring name: RENAME VARIABLE
     * Changed variable name from query => getCustomersDetails
     */
    public ResultSet getQueryResult() {
        try {
            String getCustomersDetails = "SELECT customercode AS CustomerCode, fullname AS Name, location AS Location, phone AS Phone FROM customers";
            rs = stmt.executeQuery(getCustomersDetails);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return rs;
    }//end of method getQueryResult

    /***
     * Refactoring name: RENAME VARIABLE
     * Changed variable name from query => getCustomersWithCredit
     */
    public ResultSet getCreditCustomersQueryResult() {
        try {
            String getCustomersWithCredit = "SELECT * FROM customers WHERE credit>0";
            rs = stmt.executeQuery(getCustomersWithCredit);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return rs;
    }

    /***
     * Refactoring name: RENAME VARIABLE
     * Changed variable name from query => getCustomersWithDebit
     */
    public ResultSet getDebitCustomersQueryResult() {
        try {
            String getCustomersWithDebit = "SELECT * FROM customers WHERE credit=0";
            rs = stmt.executeQuery(getCustomersWithDebit);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return rs;
    }

    /***
     * Refactoring name: RENAME VARIABLE
     * Changed variable name from query => getCustomers
     */
    public ResultSet getSearchCustomersQueryResult(String searchTxt) {
        try {
            String getCustomers = "SELECT * FROM customers WHERE fullname LIKE '%"+searchTxt+"%' OR location LIKE '%"+searchTxt+"%' OR customercode LIKE '%"+searchTxt+"%' OR phone LIKE '%"+searchTxt+"%'";
            rs = stmt.executeQuery(getCustomers);
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return rs;
    }

    /***
     * Refactoring name: RENAME VARIABLE
     * Changed variable name from query => getCustomersByCode
     */
    public ResultSet getCustomersName(String customerCode){
        try{
            String getCustomersByCode="SELECT * FROM customers WHERE customercode='"+customerCode+"'";
            rs=stmt.executeQuery(getCustomersByCode);
        }catch(Exception e){
            e.printStackTrace();
        }
        return rs;
    }

    /***
     * Refactoring name: RENAME VARIABLE
     * Changed variable name from query => getCustomersByProductCode
     */
    public ResultSet getProductsName(String productCode){
        try{
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
