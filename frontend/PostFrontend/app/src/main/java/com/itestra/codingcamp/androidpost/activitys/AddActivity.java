package com.itestra.codingcamp.androidpost.activitys;

import android.os.Bundle;
import android.widget.EditText;
import android.widget.Toast;
import android.widget.ToggleButton;

import com.itestra.codingcamp.androidpost.R;
import com.itestra.codingcamp.androidpost.exceptions.InvalidValueException;
import com.itestra.codingcamp.androidpost.exceptions.RestException;
import com.itestra.codingcamp.androidpost.exceptions.ServerException;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * Created by Toni on 23.08.2017.
 */

public class AddActivity extends BaseActivity {

    private EditText editTextSenderName;

    private EditText editTextSenderAddress;
    private EditText editTextSenderZip;
    private EditText editTextSenderCity;
    private EditText editTextReceiverName;
    private EditText editTextReceiverAddress;
    private EditText editTextReceiverZip;
    private EditText editTextReceiverCity;
    List<ToggleButton> sizeToggleButtons;
    private EditText editTextPackageWeight;

    @Override
    int getContentViewId() {
        return R.layout.activity_add;
    }

    @Override
    int getNavigationMenuItemId() {
        return R.id.navigation_add;
    }

    @Override
    void sendData() {
        HashMap<String, String> data = getPacketData();
        try {
            String id = restInterface.newPackage(data);
            Toast.makeText(this, "Registered package: "+id, Toast.LENGTH_LONG).show();
        } catch (InvalidValueException e) {
            // TODO show in GUI
            System.err.println(e.getKey() + " has error " + e.getMessage());
        } catch (ServerException e) {
            System.err.println("ServerException: " + e.getMessage());
        } catch (RestException e) {
            System.err.println("RestException: " + e.getMessage());
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void fillWithFakeData() {
        JSONObject jsonSender = fakeDataProvider.getRandomFakeData();
        JSONObject jsonReceiver = fakeDataProvider.getRandomFakeData();

        try {
            editTextSenderName.setText(jsonSender.get("name").toString());
            editTextSenderAddress.setText(jsonSender.get("street").toString());
            editTextSenderZip.setText(fakeDataProvider.getRandomFakeZip());
            editTextSenderCity.setText(jsonSender.get("city").toString());
            editTextReceiverName.setText(jsonReceiver.get("name").toString());
            editTextReceiverAddress.setText(jsonReceiver.get("street").toString());
            editTextReceiverZip.setText(fakeDataProvider.getRandomFakeZip());
            editTextReceiverCity.setText(jsonReceiver.get("city").toString());
            editTextPackageWeight.setText(jsonReceiver.get("weight").toString());
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        initToggleButtons();
        initInputs();
        fillWithFakeData();
    }

    private void initInputs() {
        editTextSenderName = (EditText) findViewById(R.id.edittext_sender_name);
        editTextSenderAddress = (EditText) findViewById(R.id.edittext_sender_address);
        editTextSenderZip = (EditText) findViewById(R.id.edittext_sender_zip);
        editTextSenderCity = (EditText) findViewById(R.id.edittext_sender_city);
        editTextReceiverName = (EditText) findViewById(R.id.edittext_receiver_name);
        editTextReceiverAddress = (EditText) findViewById(R.id.edittext_receiver_address);
        editTextReceiverZip = (EditText) findViewById(R.id.edittext_receiver_zip);
        editTextReceiverCity = (EditText) findViewById(R.id.edittext_receiver_city);
        editTextPackageWeight = (EditText) findViewById(R.id.edittext_packet_weight);
    }

    private void initToggleButtons() {
        sizeToggleButtons = new ArrayList<>();
        sizeToggleButtons.add((ToggleButton) findViewById(R.id.toggle_size_small));
        sizeToggleButtons.add((ToggleButton) findViewById(R.id.toggle_size_normal));
        sizeToggleButtons.add((ToggleButton) findViewById(R.id.toggle_size_big));

        for (ToggleButton toggleButton : sizeToggleButtons) {
            toggleButton.setOnCheckedChangeListener((buttonView, isChecked) -> {
                sizeToggleButtons.forEach(t -> {
                    t.setChecked(false);
                });
                toggleButton.setChecked(isChecked);
            });
        }
    }

    private HashMap<String, String> getPacketData() {
        HashMap<String, String> data = new HashMap<>();
        data.put("sender_name", editTextSenderName.getText().toString());
        data.put("sender_street", editTextSenderAddress.getText().toString());
        data.put("sender_zip", editTextSenderZip.getText().toString());
        data.put("sender_city", editTextSenderCity.getText().toString());
        data.put("receiver_name", editTextReceiverName.getText().toString());
        data.put("receiver_street", editTextReceiverAddress.getText().toString());
        data.put("receiver_zip", editTextReceiverZip.getText().toString());
        data.put("receiver_city", editTextReceiverCity.getText().toString());
        data.put("size", getSelectedSize());
        data.put("weight", ((EditText) findViewById(R.id.edittext_packet_weight)).getText().toString());

        return data;
    }

    private String getSelectedSize()
    {
        for (ToggleButton toggleButton : sizeToggleButtons) {
            if (toggleButton.isChecked()) {
                return(toggleButton.getTextOn().toString().toLowerCase());
            }
        }

        return "";
    }
}
