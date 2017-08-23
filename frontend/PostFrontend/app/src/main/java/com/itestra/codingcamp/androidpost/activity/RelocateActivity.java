package com.itestra.codingcamp.androidpost.activity;

import android.Manifest;
import android.content.pm.PackageManager;
import android.graphics.Typeface;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ToggleButton;

import com.google.zxing.integration.android.IntentResult;
import com.itestra.codingcamp.androidpost.R;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Toni on 23.08.2017.
 */

public class RelocateActivity extends BaseActivity{

    List<ToggleButton> toggleButtons;

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

        if(((ToggleButton) findViewById(R.id.toggleButton_car)).isChecked()) vehicle = "car";
        if(((ToggleButton) findViewById(R.id.toggleButton_plane)).isChecked()) vehicle = "plane";
        if(((ToggleButton) findViewById(R.id.toggleButton_house)).isChecked()) vehicle = "center";
        if(((ToggleButton) findViewById(R.id.toggleButton_rocket)).isChecked()) vehicle = "rocket";
        if(((ToggleButton) findViewById(R.id.toggleButton_foot)).isChecked()) vehicle = "foot";
        if(((ToggleButton) findViewById(R.id.toggleButton_ship)).isChecked()) vehicle = "ship";
        if(((ToggleButton) findViewById(R.id.toggleButton_truck)).isChecked()) vehicle = "truck";
        if(((ToggleButton) findViewById(R.id.toggleButton_train)).isChecked()) vehicle = "train";
        if(((ToggleButton) findViewById(R.id.toggleButton_failed)).isChecked()) vehicle = "failed";

        restInterface.updatePackage(id, station, vehicle);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        initScanButton();

        ((EditText)findViewById(R.id.edittext_packet_id)).setText(packet_id);

        toggleButtons = new ArrayList<>();
        toggleButtons.add((ToggleButton) findViewById(R.id.toggleButton_car));
        toggleButtons.add((ToggleButton) findViewById(R.id.toggleButton_plane));
        toggleButtons.add((ToggleButton) findViewById(R.id.toggleButton_house));
        toggleButtons.add((ToggleButton) findViewById(R.id.toggleButton_rocket));
        toggleButtons.add((ToggleButton) findViewById(R.id.toggleButton_foot));
        toggleButtons.add((ToggleButton) findViewById(R.id.toggleButton_ship));
        toggleButtons.add((ToggleButton) findViewById(R.id.toggleButton_truck));
        toggleButtons.add((ToggleButton) findViewById(R.id.toggleButton_train));
        toggleButtons.add((ToggleButton) findViewById(R.id.toggleButton_failed));

        Typeface font = Typeface.createFromAsset( getAssets(), "fontawesome-webfont.ttf" );
        for(ToggleButton toggleButton : toggleButtons){
            toggleButton.setTypeface(font);
            toggleButton.setOnCheckedChangeListener((buttonView, isChecked) -> {
                toggleButtons.forEach(t -> { t.setChecked(false);});
                toggleButton.setChecked(isChecked);
            });
        }

    }

    private void initScanButton() {
        Button scanButton = (Button) findViewById(R.id.button_scan);
        scanButton.setOnClickListener(v -> {
            if (ActivityCompat.checkSelfPermission(RelocateActivity.this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                startScan();
            } else {
                String permission = Manifest.permission.CAMERA;
                if (ContextCompat.checkSelfPermission(RelocateActivity.this, permission) != PackageManager.PERMISSION_GRANTED) {
                    ActivityCompat.requestPermissions(RelocateActivity.this, new String[]{permission}, PERMISSION_REQUEST_CODE);
                }
            }
        });
    }
}
