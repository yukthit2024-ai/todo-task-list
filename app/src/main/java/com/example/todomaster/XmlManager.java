package com.example.todomaster;

import android.content.Context;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.File;

public class XmlManager {
    public static File getFile(Context context) {
        String path = context.getSharedPreferences("Settings", Context.MODE_PRIVATE)
            .getString("storage_path", context.getFilesDir().getAbsolutePath() + "/todo_master.xml");
        return new File(path);
    }

    public static TodoMaster read(Context context) {
        TodoMaster master = new TodoMaster();
        File file = getFile(context);
        if (!file.exists()) return master;

        try {
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            Document doc = db.parse(file);
            doc.getDocumentElement().normalize();

            NodeList listNodes = doc.getElementsByTagName("todo_list");
            for (int i = 0; i < listNodes.getLength(); i++) {
                Element listElement = (Element) listNodes.item(i);
                TodoList list = new TodoList(listElement.getAttribute("name"));
                NodeList itemNodes = listElement.getElementsByTagName("item");
                for (int j = 0; j < itemNodes.getLength(); j++) {
                    Element itemElement = (Element) itemNodes.item(j);
                    list.items.add(new TodoItem(itemElement.getTextContent()));
                }
                master.lists.add(list);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return master;
    }

    public static void save(Context context, TodoMaster master) {
        try {
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            Document doc = db.newDocument();

            Element rootElement = doc.createElement("todo_master");
            doc.appendChild(rootElement);

            for (TodoList list : master.lists) {
                Element listElement = doc.createElement("todo_list");
                listElement.setAttribute("name", list.name);
                for (TodoItem item : list.items) {
                    Element itemElement = doc.createElement("item");
                    itemElement.appendChild(doc.createTextNode(item.name));
                    listElement.appendChild(itemElement);
                }
                rootElement.appendChild(listElement);
            }

            TransformerFactory tf = TransformerFactory.newInstance();
            Transformer transformer = tf.newTransformer();
            DOMSource source = new DOMSource(doc);
            StreamResult result = new StreamResult(getFile(context));
            transformer.transform(source, result);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
