package com.itestra.codingcamp.androidpost.activity;

import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.view.MenuItem;
import android.view.ViewGroup;
import android.widget.ViewSwitcher;

import com.itestra.codingcamp.androidpost.R;
import com.itestra.codingcamp.androidpost.rest.RestInterface;

import java.util.HashMap;

import view.AddView;
import view.DeliverView;
import view.RelocateView;

public class StartActivity extends AppCompatActivity {

    private ViewGroup contentViewGroup;

    private AddView addView;
    private RelocateView relocateView;
    private DeliverView deliverView;

    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {

        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            switch (item.getItemId()) {
                case R.id.navigation_add:
                    contentViewGroup.removeAllViews();
                    contentViewGroup.addView(addView);
                    return true;
                case R.id.navigation_relocate:
                    contentViewGroup.removeAllViews();
                    contentViewGroup.addView(relocateView);
                    return true;
                case R.id.navigation_deliver:
                    contentViewGroup.removeAllViews();
                    contentViewGroup.addView(deliverView);
                    return true;
            }
            return false;
        }

    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //setContentView(R.layout.activity_start);

        RestInterface rest = new RestInterface();
        //rest.deliverPacket("1");
        HashMap<String, String> data = new HashMap<>();
        data.put("sender_name", "Simon");
        data.put("sender_street", "Destouchesstr 68");
        data.put("sender_zip", "12345");
        data.put("sender_city", "München");
        data.put("receiver_name", "Simon");
        data.put("receiver_street", "Kaiserstr 68");
        data.put("receiver_zip", "12345");
        data.put("receiver_city", "Karlsruhe");
        data.put("size", "normal");
        data.put("weight", "90000");
        try {
            String id = rest.newPackage(data);
            rest.updatePackage(id, "bla", "car");
        } catch (Exception e) {
            e.printStackTrace();
        }


        /*
        contentViewGroup = (ViewGroup) findViewById(R.id.contentViewGroup);
        BottomNavigationView navigation = (BottomNavigationView) findViewById(R.id.navigation);
        navigation.setOnNavigationItemSelectedListener(mOnNavigationItemSelectedListener);

        initViews();*/
    }

    private void initViews() {
        addView = new AddView(this);
        relocateView = new RelocateView(this);
        deliverView = new DeliverView(this);
    }

}
