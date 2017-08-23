package com.itestra.codingcamp.androidpost.activity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.widget.EditText;
import android.widget.Toast;
import android.widget.ToggleButton;

import com.itestra.codingcamp.androidpost.R;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Created by Toni on 23.08.2017.
 */

public class AddActivity extends BaseActivity {

    List<ToggleButton> toggleButtons;
    JSONArray fakeDataArray;

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
            packet_id = restInterface.newPackage(data);
            Toast.makeText(this, "Registered package: "+packet_id, Toast.LENGTH_SHORT).show();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void fillWithFakeData() throws JSONException {
        int senderIndex = ThreadLocalRandom.current().nextInt(0, fakeDataArray.length());
        int receiverIndex = ThreadLocalRandom.current().nextInt(0, fakeDataArray.length());

        ((EditText) findViewById(R.id.edittext_sender_name)).setText(((JSONObject)fakeDataArray.get(senderIndex)).get("name").toString());
        ((EditText) findViewById(R.id.edittext_sender_address)).setText(((JSONObject)fakeDataArray.get(senderIndex)).get("street").toString());
        ((EditText) findViewById(R.id.edittext_sender_zip)).setText(String.format("%05d", ThreadLocalRandom.current().nextInt(1, 10000)));
        ((EditText) findViewById(R.id.edittext_sender_city)).setText(((JSONObject)fakeDataArray.get(senderIndex)).get("city").toString());
        ((EditText) findViewById(R.id.edittext_receiver_name)).setText(((JSONObject)fakeDataArray.get(receiverIndex)).get("name").toString());
        ((EditText) findViewById(R.id.edittext_receiver_address)).setText(((JSONObject)fakeDataArray.get(receiverIndex)).get("street").toString());
        ((EditText) findViewById(R.id.edittext_receiver_zip)).setText(String.format("%05d", ThreadLocalRandom.current().nextInt(1, 10000)));
        ((EditText) findViewById(R.id.edittext_receiver_city)).setText(((JSONObject)fakeDataArray.get(receiverIndex)).get("city").toString());
        ((EditText) findViewById(R.id.edittext_packet_weight)).setText(((JSONObject)fakeDataArray.get(senderIndex)).get("weight").toString());
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

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

        try {
            initFakeData();
            fillWithFakeData();
        }
        catch (Exception e)
        {
            Log.e("JSON", e.getMessage());
            Toast.makeText(this, "Fake data could not be load!", Toast.LENGTH_SHORT).show();
        }
    }

    private void initFakeData() throws IOException, JSONException {
        String jsonString = loadFakeData();
        JSONObject jsonObject = new JSONObject(jsonString);
        fakeDataArray = (JSONArray) jsonObject.get("data");
    }

    private String loadFakeData() throws IOException {

        InputStreamReader inputStreamReader = new InputStreamReader(getAssets().open("fakedata.json"), "UTF-8");
        BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
        StringBuilder stringBuilder = new StringBuilder();
        String line = "";

        while ((line = bufferedReader.readLine()) != null) {
            stringBuilder.append(line);
        }

        bufferedReader.close();
        inputStreamReader.close();

        return stringBuilder.toString();
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
