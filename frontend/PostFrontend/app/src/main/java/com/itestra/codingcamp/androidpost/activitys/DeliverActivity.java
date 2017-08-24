package com.itestra.codingcamp.androidpost.activitys;

import android.os.Bundle;
import android.widget.EditText;
import android.widget.Toast;

import com.itestra.codingcamp.androidpost.R;
import com.itestra.codingcamp.androidpost.exceptions.InvalidValueException;
import com.itestra.codingcamp.androidpost.exceptions.NoScanButtonException;
import com.itestra.codingcamp.androidpost.exceptions.RestException;
import com.itestra.codingcamp.androidpost.exceptions.ServerException;

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
        try {
            restInterface.deliverPacket(editTextPacketId.getText().toString());
            editTextPacketId.setText("");
            packet_id = "";
            Toast.makeText(this, "Packet delivered!", Toast.LENGTH_SHORT).show();
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
