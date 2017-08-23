package com.itestra.codingcamp.androidpost.activity;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.util.Log;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import com.google.zxing.integration.android.IntentResult;
import com.itestra.codingcamp.androidpost.R;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * Created by Toni on 23.08.2017.
 */

public class AddActivity extends BaseActivity {

    List<ToggleButton> toggleButtons;

    @Override
    int getContentViewId() {
        return R.layout.activity_add;
    }

    @Override
    int getNavigationMenuItemId() {
        return R.id.navigation_add;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        FloatingActionButton floatingActionButton = (FloatingActionButton) findViewById(R.id.floating_action_button_send);
        floatingActionButton.setOnClickListener(v -> {
            HashMap<String, String> data = getPacketData();
            try {
                String id = restInterface.newPackage(data);
                Toast.makeText(this, "Registered package: "+id, Toast.LENGTH_LONG).show();
            } catch (Exception e) {
                e.printStackTrace();
            }
        });

        toggleButtons = new ArrayList<>();
        toggleButtons.add((ToggleButton) findViewById(R.id.toggle_size_small));
        toggleButtons.add((ToggleButton) findViewById(R.id.toggle_size_normal));
        toggleButtons.add((ToggleButton) findViewById(R.id.toggle_size_big));

        for(ToggleButton toggleButton : toggleButtons){
            toggleButton.setOnCheckedChangeListener((buttonView, isChecked) -> {
                toggleButtons.forEach(t -> { t.setChecked(false);});
                toggleButton.setChecked(isChecked);
            });
        }
    }

    private HashMap<String,String> getPacketData() {
        HashMap<String, String> data = new HashMap<>();
        data.put("sender_name", ((EditText) findViewById(R.id.edittext_sender_name)).getText().toString());
        data.put("sender_street", ((EditText) findViewById(R.id.edittext_sender_address)).getText().toString());
        data.put("sender_zip", ((EditText) findViewById(R.id.edittext_sender_zip)).getText().toString());
        data.put("sender_city", ((EditText) findViewById(R.id.edittext_sender_city)).getText().toString());
        data.put("receiver_name", ((EditText) findViewById(R.id.edittext_receiver_name)).getText().toString());
        data.put("receiver_street", ((EditText) findViewById(R.id.edittext_receiver_address)).getText().toString());
        data.put("receiver_zip", ((EditText) findViewById(R.id.edittext_receiver_zip)).getText().toString());
        data.put("receiver_city", ((EditText) findViewById(R.id.edittext_receiver_city)).getText().toString());

        for(ToggleButton toggleButton : toggleButtons){
            if(toggleButton.isChecked())
            {
                data.put("size", toggleButton.getTextOn().toString().toLowerCase());
            }
        }
        data.put("weight", ((EditText) findViewById(R.id.edittext_packet_weight)).getText().toString());

        return data;
    }
}
