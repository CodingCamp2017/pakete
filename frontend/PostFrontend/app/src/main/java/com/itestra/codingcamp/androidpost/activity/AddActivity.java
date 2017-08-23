package com.itestra.codingcamp.androidpost.activity;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.widget.CompoundButton;
import android.widget.ToggleButton;

import com.google.zxing.integration.android.IntentResult;
import com.itestra.codingcamp.androidpost.R;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Toni on 23.08.2017.
 */

public class AddActivity extends BaseActivity {
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
            //TODO: send();
        });

        List<ToggleButton> toggleButtons = new ArrayList<>();
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
}
