package com.itestra.codingcamp.androidpost.activitys;

import android.os.Bundle;
import android.widget.EditText;
import android.widget.Toast;
import android.widget.ToggleButton;

import com.itestra.codingcamp.androidpost.R;
import com.itestra.codingcamp.androidpost.exceptions.InvalidValueException;
import com.itestra.codingcamp.androidpost.exceptions.NoScanButtonException;
import com.itestra.codingcamp.androidpost.exceptions.ResourceNotFoundException;
import com.itestra.codingcamp.androidpost.exceptions.RestException;
import com.itestra.codingcamp.androidpost.exceptions.ServerException;
import com.itestra.codingcamp.androidpost.rest.AsyncTaskResult;
import com.itestra.codingcamp.androidpost.rest.RestInterface;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by Toni on 23.08.2017.
 */

public class RelocateActivity extends BaseActivity{

    Map<String, ToggleButton> toggleButtons;

    EditText editTextPacketId;
    EditText editTextStation;

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
        String vehicle = "";

        for(Map.Entry<String, ToggleButton> entry : toggleButtons.entrySet()) {
            if(entry.getValue().isChecked()){
                vehicle = entry.getKey();
            }
        }

        int requestId = restInterface.updatePacket(editTextPacketId.getText().toString(), editTextStation.getText().toString(), vehicle, new RestInterface.ReadyHandler() {
            @Override
            public void onReady(AsyncTaskResult result) {
                try {
                    result.getResult(); // Needed because otherwise no error is thrown
                    Toast.makeText(RelocateActivity.this, "Packet relocated!", Toast.LENGTH_SHORT).show();
                }
                catch (InvalidValueException e) {
                    if (e.getKey().equals(getResources().getString(R.string.data_packet_id))) {
                        editTextPacketId.setError(e.getMessage());
                    }
                    else if (e.getKey().equals(getResources().getString(R.string.data_station))) {
                        editTextStation.setError(e.getMessage());
                    }
                    System.err.println(e.getKey() + " has error " + e.getMessage());
                } catch (ResourceNotFoundException e)
                {
                    editTextPacketId.setError(getResources().getString(R.string.invalid_value));
                } catch (ServerException e) {
                    System.err.println("ServerException: " + e.getMessage());
                } catch (RestException e) {
                    System.err.println("RestException: " + e.getMessage());
                }
                catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });

        //restInterface.cancelTask(requestId);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        initToggleButtons();
        try {
            initScanButton();
        } catch (NoScanButtonException e) {
            Toast.makeText(this, "Scan button could not be found!", Toast.LENGTH_LONG).show();
        }

        editTextPacketId = (EditText)findViewById(R.id.edittext_packet_id);
        editTextPacketId.setText(packet_id);
        editTextStation = (EditText)findViewById(R.id.edittext_packet_station);
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
            entry.getValue().setOnClickListener(v -> {
                toggleButtons.values().forEach(t -> { t.setChecked(false);});
                entry.getValue().setChecked(true);
            });
        }
    }
}
