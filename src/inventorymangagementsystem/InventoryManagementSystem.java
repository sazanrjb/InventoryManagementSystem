/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package inventorymangagementsystem;

import com.inventory.ui.LoginDialog;
import com.jtattoo.plaf.hifi.HiFiLookAndFeel;
import java.util.Properties;
import javax.swing.JFrame;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

/**
 *
 * @author ADMIN
 */
public class InventoryManagementSystem {

    /**
     * @param args the command line arguments
     */
    public InventoryManagementSystem(int a){
    /*    if(a==1){
            try{
                Properties p=new Properties();
                p.put("logoString","IMS");
                HiFiLookAndFeel.setCurrentTheme(p);
                UIManager.setLookAndFeel("com.jtattoo.plaf.hifi.HiFiLookAndFeel");  
           }catch(ClassNotFoundException | InstantiationException | IllegalAccessException | UnsupportedLookAndFeelException e){
               e.printStackTrace();
           }
        }else if(a==2){
            try{
                Properties p=new Properties();
                p.put("logoString","IMS");
                GraphiteLookAndFeel.setCurrentTheme(p);
                UIManager.setLookAndFeel("com.jtattoo.plaf.graphite.GraphiteLookAndFeel");
           }catch(ClassNotFoundException | InstantiationException | IllegalAccessException | UnsupportedLookAndFeelException e){
               e.printStackTrace();
           }
        } */
    }

    public static void main(String[] args) {
     //   f.setIconImage(Toolkit.getDefaultToolkit().getImage(ClassLoader.getSystemResource("/images/addPeople.png")));  
            try{
                Properties p=new Properties();
                p.put("logoString","IMS");
                HiFiLookAndFeel.setCurrentTheme(p);
                //UIManager.setLookAndFeel("com.jtattoo.plaf.hifi.HiFiLookAndFeel");  
                UIManager.setLookAndFeel("com.jtattoo.plaf.acryl.AcrylLookAndFeel");  
            }catch(ClassNotFoundException | InstantiationException | IllegalAccessException | UnsupportedLookAndFeelException e){
               e.printStackTrace();
            }
        

        LoginDialog ld=new LoginDialog();
        ld.setLocationRelativeTo(null);
        ld.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        ld.setVisible(true);
        //com.sun.java.swing.plaf.nimbus.NimbusLookAndFeel
    }
    
}
