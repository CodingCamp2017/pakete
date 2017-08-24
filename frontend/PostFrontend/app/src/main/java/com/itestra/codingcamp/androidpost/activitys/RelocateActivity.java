package com.itestra.codingcamp.androidpost.activitys;

import android.graphics.Typeface;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.Toast;
import android.widget.ToggleButton;

import com.itestra.codingcamp.androidpost.R;
import com.itestra.codingcamp.androidpost.exceptions.NoScanButtonException;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by Toni on 23.08.2017.
 */

public class RelocateActivity extends BaseActivity{

    Map<String, ToggleButton> toggleButtons;

    @Override
    int getContentViewId() {
        return R.layout.activity_relocate;
    }

    @Override
    int getNavigationMenuItemId() {
        return R.id.navigation_relocate;
    }

    @Override
    void sendData() {
        String id = ((EditText)findViewById(R.id.edittext_packet_id)).getText().toString();
        String station = ((EditText)findViewById(R.id.edittext_packet_station)).getText().toString();

        String vehicle = "";

        for(Map.Entry<String, ToggleButton> entry : toggleButtons.entrySet()) {
            if(entry.getValue().isChecked()){
                vehicle = entry.getKey();
            }
        }

        restInterface.updatePackage(id, station, vehicle);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        try {
            initScanButton();
        } catch (NoScanButtonException e) {
            Toast.makeText(this, "Scan button could not be found!", Toast.LENGTH_LONG).show();
        }
        initToggleButtons();

        ((EditText)findViewById(R.id.edittext_packet_id)).setText(packet_id);
    }

    private void initToggleButtons() {
        toggleButtons = new HashMap<>();
        toggleButtons.put(getResources().getString(R.string.car), (ToggleButton) findViewById(R.id.toggleButton_car));
        toggleButtons.put(getResources().getString(R.string.plane), (ToggleButton) findViewById(R.id.toggleButton_plane));
        toggleButtons.put(getResources().getString(R.string.center),(ToggleButton) findViewById(R.id.toggleButton_center));
        toggleButtons.put(getResources().getString(R.string.rocket),(ToggleButton) findViewById(R.id.toggleButton_rocket));
        toggleButtons.put(getResources().getString(R.string.foot),(ToggleButton) findViewById(R.id.toggleButton_foot));
        toggleButtons.put(getResources().getString(R.string.ship),(ToggleButton) findViewById(R.id.toggleButton_ship));
        toggleButtons.put(getResources().getString(R.string.truck),(ToggleButton) findViewById(R.id.toggleButton_truck));
        toggleButtons.put(getResources().getString(R.string.train),(ToggleButton) findViewById(R.id.toggleButton_train));
        toggleButtons.put(getResources().getString(R.string.failed),(ToggleButton) findViewById(R.id.toggleButton_failed));

        for(Map.Entry<String, ToggleButton> entry : toggleButtons.entrySet()){
            entry.getValue().setTypeface(fontawesomeProvider.getFontawesome());
            entry.getValue().setOnCheckedChangeListener((buttonView, isChecked) -> {
                toggleButtons.values().forEach(t -> { t.setChecked(false);});
                entry.getValue().setChecked(isChecked);
            });
        }
    }
}
