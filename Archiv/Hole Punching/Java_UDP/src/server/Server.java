package server;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.lang.reflect.Array;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

/**
 * 
 * Spielt den Server eines einfachen UDP Holepunching Tests. 
 * Die Sicherstellung der Verbindung läuft ab dem Holepunch durch periodische Nachrichten.
 * Als Port wird 4567 verwendet.
 */

public class Server {
	/** Hier wird oeff. Adresse und Port des Logins gespeichert**/
	static Set<String[]> logins = new HashSet<String[]>();
	/** Socket fuer UDP Verbindung**/
	private static DatagramSocket dsocket;
	/** Array zum Empfange der Daten am Socket**/
	private static byte[] bytes;
	
	/** Initialisierung des Sockets, sowie "dauerhaftes Lauschen auf neue Clients."**/
	public static void main(String[] args) {
		bytes = new byte[1024];
		try {
			dsocket = new DatagramSocket(4567);
			while(true) {
				receive();
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	/** Liest Nachricht des Clients aus: Je nachdem ob L(ogin) oder R(eload), wird Aktion ausgeführt, ansonsten nichts.
	 *  Koennte durch mehrere Nachrichten erweitert werden, 
	 *  welche den Status des Clients aufzeichen (z.B. gerade verbunden, abgemeldet oder Aehnliches).
	 */
	private static void receive() throws Exception{
		DatagramPacket pr = new DatagramPacket(bytes, bytes.length);
		dsocket.receive(pr);
		String host = pr.getAddress().getHostAddress() + ""; 
		String port = pr.getPort() + "";

		switch(new String(bytes).charAt(0)){
			/** Bei einem Login fuegt der Server einfach dem Set hinzu**/
			case 'L':
				logins.add(new String[]{host, port});
		        break;
		    
		    /** Bei einem Reload versucht er das Set (ohne den Anfragenden) ueber UDP an den anfragenden Client zu verteilen. 
		     * (leider nicht auf max. Groesse und Fehlerhaftigkeit ueberprueft).
		     */
			case 'R':
				ByteArrayOutputStream baos = new ByteArrayOutputStream(1024);
				ObjectOutputStream oos = new ObjectOutputStream(baos);
				Set<String[]> only = logins;
				for (Iterator<String[]> i = only.iterator(); i.hasNext();) {
				    String[] element = i.next();
				    if (element[0].equals(host) && element[1].equals(port)) {
				        i.remove();
				    }
				}
				oos.writeObject(only);
				oos.flush();
				byte[] data = baos.toByteArray();
				DatagramPacket ps = new DatagramPacket(data, data.length, InetAddress.getByName(host), Integer.parseInt(port));
				dsocket.send(ps);
				break;
		}
	}
	
}
