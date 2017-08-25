package com.itestra.codingcamp.androidpost.activitys;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.os.AsyncTask;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import com.itestra.codingcamp.androidpost.R;
import com.itestra.codingcamp.androidpost.exceptions.InvalidValueException;
import com.itestra.codingcamp.androidpost.exceptions.RestException;
import com.itestra.codingcamp.androidpost.exceptions.ServerException;
import com.itestra.codingcamp.androidpost.rest.AsyncTaskResult;
import com.itestra.codingcamp.androidpost.rest.RestInterface;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by Toni on 23.08.2017.
 */

public class AddActivity extends BaseActivity {

    private Map<String, TextView> inputMap;

    List<ToggleButton> sizeToggleButtons;

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

        AlertDialog dialog = getProcessingDialog();

        int requestId = restInterface.newPacket(data, new RestInterface.ReadyHandler() {
            @Override
            public void onReady(AsyncTaskResult result) {
                try {
                    packet_id = result.getResult().getString("id");
                    Toast.makeText(AddActivity.this, "Registered package: "+packet_id, Toast.LENGTH_LONG).show();
                } catch (InvalidValueException e) {
                    inputMap.get(e.getKey()).setError(e.getMessage());
                    System.err.println(e.getKey() + " has error " + e.getMessage());
                    Toast.makeText(AddActivity.this, "There was an error in the field " + e.getKey(), Toast.LENGTH_LONG).show();
                } catch (ServerException e) {
                    System.err.println("ServerException: " + e.getMessage());
                    Toast.makeText(AddActivity.this, "ServerException: " + e.getMessage(), Toast.LENGTH_LONG).show();
                } catch (RestException e) {
                    System.err.println("RestException: " + e.getMessage());
                    Toast.makeText(AddActivity.this, "RestException: " + e.getMessage(), Toast.LENGTH_LONG).show();
                }
                catch (Exception e) {
                    e.printStackTrace();
                }

                dialog.dismiss();
            }
        });

        dialog.setButton(AlertDialog.BUTTON_NEGATIVE, "Cancel",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        restInterface.cancelTask(requestId);
                        dialog.dismiss();
                    }
                });
        dialog.show();
    }

    private void fillWithFakeData() {
        JSONObject jsonSender = fakeDataProvider.getRandomFakeData();
        JSONObject jsonReceiver = fakeDataProvider.getRandomFakeData();

        try {
            inputMap.get(getResources().getString(R.string.data_sender_name)).setText(jsonSender.get("name").toString());
            inputMap.get(getResources().getString(R.string.data_sender_street)).setText(jsonSender.get("street").toString());
            inputMap.get(getResources().getString(R.string.data_sender_zip)).setText(fakeDataProvider.getRandomFakeZip());
            inputMap.get(getResources().getString(R.string.data_sender_city)).setText(jsonSender.get("city").toString());
            inputMap.get(getResources().getString(R.string.data_receiver_name)).setText(jsonReceiver.get("name").toString());
            inputMap.get(getResources().getString(R.string.data_receiver_street)).setText(jsonReceiver.get("street").toString());
            inputMap.get(getResources().getString(R.string.data_receiver_zip)).setText(fakeDataProvider.getRandomFakeZip());
            inputMap.get(getResources().getString(R.string.data_receiver_city)).setText(jsonReceiver.get("city").toString());
            inputMap.get(getResources().getString(R.string.data_weight)).setText(jsonReceiver.get("weight").toString());
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
        inputMap = new HashMap<>();
        inputMap.put(getResources().getString(R.string.data_sender_name), (EditText) findViewById(R.id.edittext_sender_name));
        inputMap.put(getResources().getString(R.string.data_sender_street), (EditText) findViewById(R.id.edittext_sender_address));
        inputMap.put(getResources().getString(R.string.data_sender_zip), (EditText) findViewById(R.id.edittext_sender_zip));
        inputMap.put(getResources().getString(R.string.data_sender_city), (EditText) findViewById(R.id.edittext_sender_city));
        inputMap.put(getResources().getString(R.string.data_receiver_name), (EditText) findViewById(R.id.edittext_receiver_name));
        inputMap.put(getResources().getString(R.string.data_receiver_street), (EditText) findViewById(R.id.edittext_receiver_address));
        inputMap.put(getResources().getString(R.string.data_receiver_zip), (EditText) findViewById(R.id.edittext_receiver_zip));
        inputMap.put(getResources().getString(R.string.data_receiver_city), (EditText) findViewById(R.id.edittext_receiver_city));
        inputMap.put(getResources().getString(R.string.data_weight), (EditText) findViewById(R.id.edittext_packet_weight));
    }

    private void initToggleButtons() {
        sizeToggleButtons = new ArrayList<>();
        sizeToggleButtons.add((ToggleButton) findViewById(R.id.toggle_size_small));
        sizeToggleButtons.add((ToggleButton) findViewById(R.id.toggle_size_normal));
        sizeToggleButtons.add((ToggleButton) findViewById(R.id.toggle_size_big));

        for (ToggleButton toggleButton : sizeToggleButtons) {
            toggleButton.setOnClickListener(v -> {
                sizeToggleButtons.forEach(t -> {
                    t.setChecked(false);
                });
                toggleButton.setChecked(true);
            });
        }
    }

    private HashMap<String, String> getPacketData() {
        HashMap<String, String> data = new HashMap<>();
        for (Map.Entry<String, TextView> entry : inputMap.entrySet()) {
            if(entry.getValue() instanceof EditText)
            {
                data.put(entry.getKey(), entry.getValue().getText().toString());
            }
        }
        data.put("size", getSelectedSize());

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
