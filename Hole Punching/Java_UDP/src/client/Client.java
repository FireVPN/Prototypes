package client;

import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.JTextField;

/**
 * Spielt den Client eines einfachen UDP Holepunching Tests. 
 * Die Sicherstellung der Verbindung läuft ab dem Holepunch durch periodische Nachrichten.
 * Als Port wird 4567 verwendet.
 */
public class Client {
	private static InetAddress server;
	private static DatagramSocket socket;
	private final JTextField field;
	
	public static void main(String[] args) {
		new Client();
	}
	
	public Client(){
		try {
			/** Initialisierung**/
			/** IP des Server eintragen **/
			server = InetAddress.getByName("0.0.0.0");
			socket = new DatagramSocket();
		} catch (UnknownHostException | SocketException e1) {
			e1.printStackTrace();
		}
		
		/** Verbindung zum Server aufbauen**/
		connect();
		
		/** GUI nur fuer Testing **/
		final JFrame frame = new JFrame();
		final JPanel main = new JPanel(new GridLayout(3, 3));
		final JButton reload = new JButton("Aktualisieren");
		final JButton start = new JButton("Starten");
		final JComboBox box = new JComboBox();
		final JTextArea area = new JTextArea();
		field = new JTextField();
		area.setSize(50, 50);
		
		reload.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				box.removeAllItems();
				for(String i: reload())
					box.addItem(i);
				frame.validate();
			}
		});
		
		start.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String selected = (String) box.getSelectedItem();
				String[] selectedElements = selected.split(",");
				try{
				send(InetAddress.getByName(selectedElements[0].substring(1)),Integer.parseInt(selectedElements[1].substring(1, selectedElements[1].length()-1)), area);
				}catch(Exception e2){
					System.out.println("Something went wrong");
					e2.printStackTrace();
				}
			}
		});
		
		main.add(reload);
		main.add(start);
		main.add(box);
		main.add(area);
		main.add(field);
		frame.add(main);
		frame.setTitle("Client");
		frame.setSize(500,500);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setVisible(true);
	}
	
	/** Schickt Login-Signal an angegebenen Server **/
	private static void connect(){
		try{
			byte[] bytes;
			bytes = "L".getBytes();
			DatagramPacket packet = new DatagramPacket(bytes, bytes.length, server, 4567);
			socket.send(packet);
		}catch (Exception e){
			e.printStackTrace();
		}
	}
	
	/** Schickt das Signal fuer eine Listenaktualisierung an den Server**/
	private static String[] reload(){
		try{
			byte[] bytes;
			bytes = "R".getBytes();
			DatagramPacket packet = new DatagramPacket(bytes, bytes.length, server, 4567);
			socket.send(packet);
			
			byte[] buffer = new byte[1024];
			packet = new DatagramPacket(buffer, buffer.length );
			socket.receive(packet);
			
			/** Hier gab es ein Problem mit der Objektuebertragung, habe ich durch
			 * einen einfachen Iterator behoben.
			 */
			ByteArrayInputStream baos = new ByteArrayInputStream(buffer);
		    ObjectInputStream oos = new ObjectInputStream(baos);
		    Set<String[]> logins = (HashSet<String[]>) oos.readObject();
		    String[] formed = new String[logins.size()];
		    
		    int i =0;
		    for(Iterator<String[]> itr = logins.iterator(); itr.hasNext();){
		    	String cache = Arrays.toString(itr.next());
		    	formed[i] = cache;
		    	i++;
		    }
		    
		    return formed;
		} catch (Exception e){
			e.printStackTrace();
		}
		return new String[]{"Something went wrong."};
	}
	
	/** Der eigentliche Sendevorgang an den gewuenschten Client. Hierzu wird aus der Liste einer ausgewaehlt. 
	 * Natuerlich funktioniert dies aber erst nachdem BEIDE die erste Nachricht gesendet haben (Holepunching Theorie).
	 * @param addr Adresse des Hosts
	 * @param port Port des Hosts
	 * @param area TextArea fuer Testing
	 */
	private void send(final InetAddress addr, final int port, final JTextArea area){
		/** Thread welcher den Empang von Nachrichten uebernimmt.**/
		Thread in = new Thread() {
			public void run() {
				while (true) {
					byte[] bytes = new byte[1024];
					DatagramPacket packet = new DatagramPacket(bytes,
							bytes.length);
					try {
						socket.receive(packet);
						bytes = Arrays
								.copyOfRange(bytes, 0, packet.getLength());
						String s = new String(bytes);
						area.append(s + "\n");
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
			}
		};
		in.start();
		/** Thread welcher das Senden von Nachrichten uebernimmt.**/
		Thread out = new Thread(){
			public void run() {
				while (true) {
					byte[] b = field.getText().getBytes();
					try {
						DatagramPacket packet = new DatagramPacket(b, b.length,
								addr, port);
						socket.send(packet);
						Thread.sleep(1000);
					} catch (Exception e) {
						e.printStackTrace();
					}
				}
			}
		};
		out.start();
		
	}
}
