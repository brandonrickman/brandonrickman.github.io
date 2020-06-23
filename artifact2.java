/**
 * Author: Brandon Rickman
 * Southern New Hampshire University
 * IT145 - Application Development
 * Final Project: Zoo Authentication (Option 1)
 * @Brandon.Rickman@snhu.edu
 */
import java.util.Scanner; // Scanner class import
import java.io.FileInputStream; // FileInputStream class import
import java.io.IOException; // IOException for FileInputStream

public class ZooAuthentication {
    public static void main(String[] args) throws IOException {

        Scanner scnr = new Scanner(System.in); // new instance of input scanner
        FileInputStream fileRoleStream = null; // open file stream reader
        HashCompare compare = new HashCompare(); // new instance of HashCompare class
        
        // intialize all vars needed
        String userName;
        String userPassWord;
        String userPassHash;
        String credUserName; 
        String credPassHash;
        String credRole;
        int attemptCounter = 1;
        final int attemptMax = 3; // set to final int due to max number being a set amount
        boolean inputDone = false;
        
        while ( !inputDone ) // starts an input loop
        {
            while ( attemptCounter <= attemptMax ) // starts a loop for attempts if number of attempts is less than max attempts
            {
                // welcome start up print out.
                System.out.println("\nWELCOME TO METRO ZOONET!\n");
                System.out.println("------------------------");
                System.out.println("You only have three attempts to enter the "
                        + "correct credentials.");
                System.out.println("------------------------");
                System.out.println("\nType LOGIN to provide credentials or type LOGOUT to log off system completely.");
                String entry = scnr.nextLine(); // user input if they would like to login or log out
                entry = entry.toUpperCase(); // converts user input to uppercase
                
                // if/else statement for login
                if ( entry.equals("LOGIN") ) // request user input
                {
                    System.out.println("\nPlease enter your Username: ");
                    userName = scnr.nextLine(); // user input of username
                    System.out.println("Please enter your Password: ");
                    userPassWord = scnr.nextLine(); // user input of password
                }   
                else if ( entry.equals("LOGOUT") ) // breaks login loop
                {
                    System.out.println("You have successfully LOGGED out. Goodbye!");
                    break;
                }
                else // breaks login loop
                {
                    System.out.println("You are NOT authorized. Goodbye!");
                    break;
                }
                
                //Class method call to create Hashed Password and get credentials parts from file
                compare.setCreds(); // runs method in HashCompare to set the array credentials in file
                compare.getCred(userName); // runs method in HashCompare to get credentials.
                userPassHash = compare.hashPassword(userPassWord); // covert user entered password to hash usering MD5 hash
                // get each part from credentials file
                credUserName = compare.getCredUserName();
                credPassHash = compare.getCredPassHash();
                credRole = compare.getCredRole();
                
                // if creds username is nothing or method to compare password is false. Prints out Error Message.
                if ( (credUserName == null) || (!compare.comparePassword(userPassHash, credPassHash)) )
                {
                    System.out.println("\n--------------------");
                    System.out.println("I'm sorry you have entered the wrong username "
                            + "or password. Please try again.");
                    System.out.println("--------------------");
                    System.out.printf("\nYou have used %d of 3 attempts at logging in.\n", attemptCounter);
                    
                    // if attempt number is equal to max attemtps break out of loop, denying access to system.
                    if (attemptCounter == attemptMax)
                    {
                        break;
                    }
                    else // increments num of attempts if not equal to max attempts
                    {
                        attemptCounter++;
                    }
                }
                else // if cred username has value or compared user hash and creds hash is true
                {
                    attemptCounter = 1; // reset attempt counter
                    String fileRole = "Zoo Authentication/" + credRole + ".txt"; // creates a string to call later using cred Role.
                    System.out.println("");
                    // finds the file for the specific Role
                    fileRoleStream = new FileInputStream(fileRole); // creates new instance of Role file reader
                    Scanner roleFS = new Scanner(fileRoleStream); // new scanner to parse Role file

                    while (roleFS.hasNext()) // while specific Role file has more elements...
                    {
                        System.out.println(roleFS.nextLine()); // print those lines to the screen for user
                    }
                    System.out.println("");
                    
                    // new prompt for logout
                    boolean logOutPrompt = true;
                    while (logOutPrompt) // starts new loop for logout input
                    {
                        System.out.println("Log Out? (Type Y for yes)");
                        Scanner logOutScnr = new Scanner(System.in); // new scanner for Logout after file read
                        String logOut = logOutScnr.next(); // user input for logout
                        
                        // if user input does not equal Y or y. Print Error message and request user input again
                        if ( (!logOut.equals("Y")) && (!logOut.equals("y")) )
                        {
                            System.out.println("Please Re-Try Entry.\n");
                        }
                        else // user input does equal Y or y. 
                        {
                            System.out.println("");
                            logOutPrompt = false; // end logout loop
                        }
                        fileRoleStream.close(); // close Role file reader
                    }
                }
            }
            inputDone = true; // end input loop and close program
            scnr.close();
        }
    }
    
}
