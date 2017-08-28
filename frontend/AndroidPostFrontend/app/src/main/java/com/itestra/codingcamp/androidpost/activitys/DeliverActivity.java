package com.itestra.codingcamp.androidpost.activitys;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.Toast;

import com.itestra.codingcamp.androidpost.R;
import com.itestra.codingcamp.androidpost.exceptions.InvalidValueException;
import com.itestra.codingcamp.androidpost.exceptions.NetworkException;
import com.itestra.codingcamp.androidpost.exceptions.NoScanButtonException;
import com.itestra.codingcamp.androidpost.exceptions.ResourceNotFoundException;
import com.itestra.codingcamp.androidpost.exceptions.RestException;
import com.itestra.codingcamp.androidpost.exceptions.ServerException;
import com.itestra.codingcamp.androidpost.rest.AsyncTaskResult;
import com.itestra.codingcamp.androidpost.rest.RestInterface;

import java.util.HashMap;

/**
 * Created by Toni on 23.08.2017.
 */

public class DeliverActivity extends BaseActivity {

    private EditText editTextPacketId;

    @Override
    int getContentViewId() {
        return R.layout.activity_deliver;
    }

    @Override
    int getNavigationMenuItemId() {
        return R.id.navigation_deliver;
    }

    @Override
    void sendData() {
        ProgressDialog dialog = ProgressDialog.show(this, "Anfrage wird verarbeitet", "Paket wird ausgeliefert");
        dialog.setCancelable(false);

        restInterface.deliverPacket(editTextPacketId.getText().toString(), new RestInterface.ReadyHandler() {
            @Override
            public void onReady(AsyncTaskResult result) {
                try {
                    result.getResult(); // Needed because otherwise no error is thrown
                    editTextPacketId.setText("");
                    packet_id = "";
                    Toast.makeText(DeliverActivity.this, "Packet delivered!", Toast.LENGTH_SHORT).show();
                }
                catch (ResourceNotFoundException e)
                {
                    editTextPacketId.setError(e.getMessage());
                    Toast.makeText(DeliverActivity.this, e.getMessage() , Toast.LENGTH_LONG).show();
                }
                catch (InvalidValueException e) {
                    if (e.getKey().equals(getResources().getString(R.string.data_packet_id))) {
                        editTextPacketId.setError(e.getMessage());
                    }
                    System.err.println(e.getKey() + " has error " + e.getMessage());
                    Toast.makeText(DeliverActivity.this, e.getKey() + " has error " + e.getMessage() , Toast.LENGTH_LONG).show();
                } catch (ServerException e) {
                    System.err.println("ServerException: " + e.getMessage());
                    Toast.makeText(DeliverActivity.this, "ServerException: " + e.getMessage(), Toast.LENGTH_LONG).show();
                } catch (NetworkException e) {
                    System.err.println("NetworkException: " + e.getMessage());
                    Toast.makeText(DeliverActivity.this, "Network failed, please check your connection: " + e.getMessage(), Toast.LENGTH_LONG).show();
                } catch (RestException e) {
                    System.err.println("RestException: " + e.getMessage());
                    Toast.makeText(DeliverActivity.this, "RestException: " + e.getMessage(), Toast.LENGTH_LONG).show();
                }
                catch (Exception e) {
                    e.printStackTrace();
                    Toast.makeText(DeliverActivity.this, "Unknown error", Toast.LENGTH_SHORT).show();
                }

                dialog.dismiss();
            }
        });
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        try {
            initScanButton();
        } catch (NoScanButtonException e) {
            Toast.makeText(this, "Scan button could not be found!", Toast.LENGTH_LONG).show();
        }

        editTextPacketId = ((EditText) findViewById(R.id.edittext_packet_id));
        editTextPacketId.setText(packet_id);
    }

}
