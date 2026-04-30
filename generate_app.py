import os

base_dir = "x:/Projects_X/0_Active/8_Android_APK/Tasks_APK_GITHUB/app/src/main"
java_dir = os.path.join(base_dir, "java/com/example/todomaster")
res_dir = os.path.join(base_dir, "res")

os.makedirs(java_dir, exist_ok=True)
os.makedirs(os.path.join(res_dir, "layout"), exist_ok=True)
os.makedirs(os.path.join(res_dir, "values"), exist_ok=True)
os.makedirs(os.path.join(res_dir, "menu"), exist_ok=True)
os.makedirs(os.path.join(res_dir, "xml"), exist_ok=True)

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# AndroidManifest.xml
write_file(os.path.join(base_dir, "AndroidManifest.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.todomaster">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="32" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.TodoMaster"
        android:usesCleartextTraffic="true">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.TodoMaster.NoActionBar">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""")

# build.gradle
write_file("x:/Projects_X/0_Active/8_Android_APK/Tasks_APK_GITHUB/app/build.gradle", """
plugins {
    id 'com.android.application'
}

android {
    namespace 'com.example.todomaster'
    compileSdk 34

    defaultConfig {
        applicationId "com.example.todomaster"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.recyclerview:recyclerview:1.3.2'
    
    // Retrofit & Gson
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
}
""")

# Java Classes

# Models
write_file(os.path.join(java_dir, "TodoItem.java"), """
package com.example.todomaster;

public class TodoItem {
    public String name;
    public TodoItem() {}
    public TodoItem(String name) { this.name = name; }
}
""")

write_file(os.path.join(java_dir, "TodoList.java"), """
package com.example.todomaster;
import java.util.ArrayList;
import java.util.List;

public class TodoList {
    public String name;
    public List<TodoItem> items = new ArrayList<>();
    public TodoList() {}
    public TodoList(String name) { this.name = name; }
}
""")

write_file(os.path.join(java_dir, "TodoMaster.java"), """
package com.example.todomaster;
import java.util.ArrayList;
import java.util.List;

public class TodoMaster {
    public List<TodoList> lists = new ArrayList<>();
}
""")

# XML Manager
write_file(os.path.join(java_dir, "XmlManager.java"), """
package com.example.todomaster;

import android.content.Context;
import android.util.Log;
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
""")

write_file(os.path.join(java_dir, "MainActivity.java"), """
package com.example.todomaster;

import android.os.Bundle;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.drawerlayout.widget.DrawerLayout;
import com.google.android.material.navigation.NavigationView;
import androidx.core.view.GravityCompat;
import androidx.fragment.app.Fragment;

public class MainActivity extends AppCompatActivity {
    private DrawerLayout drawer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        drawer = findViewById(R.id.drawer_layout);
        NavigationView navigationView = findViewById(R.id.nav_view);

        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(this, drawer, toolbar,
                R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();

        navigationView.setNavigationItemSelectedListener(item -> {
            Fragment fragment = null;
            int id = item.getItemId();
            if (id == R.id.nav_main) {
                fragment = new MainFragment();
            } else if (id == R.id.nav_settings) {
                fragment = new SettingsFragment();
            } else if (id == R.id.nav_matrix) {
                fragment = new MatrixFragment();
            } else if (id == R.id.nav_groups) {
                fragment = new GroupsFragment();
            } else if (id == R.id.nav_help) {
                fragment = new HelpFragment();
            } else if (id == R.id.nav_about) {
                fragment = new AboutFragment();
            }

            if (fragment != null) {
                getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container, fragment).commit();
            }
            drawer.closeDrawer(GravityCompat.START);
            return true;
        });

        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction().replace(R.id.fragment_container, new MainFragment()).commit();
            navigationView.setCheckedItem(R.id.nav_main);
        }
    }
    
    @Override
    public void onBackPressed() {
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }
}
""")

write_file(os.path.join(java_dir, "MainFragment.java"), """
package com.example.todomaster;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import androidx.fragment.app.Fragment;

public class MainFragment extends Fragment {
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_main, container, false);
    }
}
""")
write_file(os.path.join(java_dir, "SettingsFragment.java"), """
package com.example.todomaster;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import androidx.fragment.app.Fragment;

public class SettingsFragment extends Fragment {
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_settings, container, false);
    }
}
""")
write_file(os.path.join(java_dir, "MatrixFragment.java"), """
package com.example.todomaster;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import androidx.fragment.app.Fragment;

public class MatrixFragment extends Fragment {
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_matrix, container, false);
    }
}
""")
write_file(os.path.join(java_dir, "GroupsFragment.java"), """
package com.example.todomaster;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import androidx.fragment.app.Fragment;

public class GroupsFragment extends Fragment {
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_groups, container, false);
    }
}
""")
write_file(os.path.join(java_dir, "HelpFragment.java"), """
package com.example.todomaster;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import androidx.fragment.app.Fragment;

public class HelpFragment extends Fragment {
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_help, container, false);
    }
}
""")
write_file(os.path.join(java_dir, "AboutFragment.java"), """
package com.example.todomaster;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import androidx.fragment.app.Fragment;

public class AboutFragment extends Fragment {
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_about, container, false);
    }
}
""")

# Layouts
write_file(os.path.join(res_dir, "layout/activity_main.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<androidx.drawerlayout.widget.DrawerLayout 
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:id="@+id/drawer_layout"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical">

        <androidx.appcompat.widget.Toolbar
            android:id="@+id/toolbar"
            android:layout_width="match_parent"
            android:layout_height="?attr/actionBarSize"
            android:background="?attr/colorPrimary"
            app:titleTextColor="@android:color/white" />

        <FrameLayout
            android:id="@+id/fragment_container"
            android:layout_width="match_parent"
            android:layout_height="match_parent" />
    </LinearLayout>

    <com.google.android.material.navigation.NavigationView
        android:id="@+id/nav_view"
        android:layout_width="wrap_content"
        android:layout_height="match_parent"
        android:layout_gravity="start"
        app:menu="@menu/drawer_menu" />

</androidx.drawerlayout.widget.DrawerLayout>
""")

write_file(os.path.join(res_dir, "layout/fragment_main.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Main TO-DO Lists" android:textSize="20sp" />
</LinearLayout>
""")
write_file(os.path.join(res_dir, "layout/fragment_settings.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Settings" android:textSize="20sp" />
</LinearLayout>
""")
write_file(os.path.join(res_dir, "layout/fragment_matrix.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Matrix Credentials" android:textSize="20sp" />
</LinearLayout>
""")
write_file(os.path.join(res_dir, "layout/fragment_groups.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Groups / Rooms" android:textSize="20sp" />
</LinearLayout>
""")
write_file(os.path.join(res_dir, "layout/fragment_help.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="Help" android:textSize="20sp" />
</LinearLayout>
""")
write_file(os.path.join(res_dir, "layout/fragment_about.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="About" android:textSize="20sp" />
</LinearLayout>
""")

# menu
write_file(os.path.join(res_dir, "menu/drawer_menu.xml"), """
<?xml version="1.0" encoding="utf-8"?>
<menu xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:id="@+id/nav_main" android:title="Main" />
    <item android:id="@+id/nav_settings" android:title="Settings" />
    <item android:id="@+id/nav_matrix" android:title="Matrix Credentials" />
    <item android:id="@+id/nav_groups" android:title="Groups / Rooms" />
    <item android:id="@+id/nav_help" android:title="Help" />
    <item android:id="@+id/nav_about" android:title="About" />
</menu>
""")

# values
write_file(os.path.join(res_dir, "values/strings.xml"), """
<resources>
    <string name="app_name">Todo Master</string>
    <string name="navigation_drawer_open">Open navigation drawer</string>
    <string name="navigation_drawer_close">Close navigation drawer</string>
</resources>
""")

write_file(os.path.join(res_dir, "values/themes.xml"), """
<resources xmlns:tools="http://schemas.android.com/tools">
    <style name="Theme.TodoMaster" parent="Theme.MaterialComponents.DayNight.DarkActionBar">
        <item name="colorPrimary">@color/purple_500</item>
        <item name="colorPrimaryDark">@color/purple_700</item>
        <item name="colorAccent">@color/teal_200</item>
    </style>
    <style name="Theme.TodoMaster.NoActionBar">
        <item name="windowActionBar">false</item>
        <item name="windowNoTitle">true</item>
    </style>
</resources>
""")

write_file(os.path.join(res_dir, "values/colors.xml"), """
<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
""")

print("Project generated successfully.")
