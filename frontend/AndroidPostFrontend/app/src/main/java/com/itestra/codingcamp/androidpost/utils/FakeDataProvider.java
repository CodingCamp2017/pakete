package com.itestra.codingcamp.androidpost.utils;

import android.content.Context;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Created by Toni on 24.08.2017.
 */

public class FakeDataProvider {

    static JSONArray fakeDataArray = null;
    private Context context;

    public FakeDataProvider(Context context){
        this.context = context;
        if(fakeDataArray == null) {
            try {
                String jsonString = loadFakeData();
                JSONObject jsonObject = new JSONObject(jsonString);
                fakeDataArray = (JSONArray) jsonObject.get("data");
            } catch (JSONException | IOException e) {
                e.printStackTrace();
            }
        }
    }

    private String loadFakeData() throws IOException {
        InputStreamReader inputStreamReader = new InputStreamReader(context.getAssets().open("fakedata.json"), "UTF-8");
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

    public JSONObject getRandomFakeData()
    {
        int randomIndex = ThreadLocalRandom.current().nextInt(0, fakeDataArray.length());
        JSONObject fakeData = null;

        try {
            fakeData = (JSONObject) fakeDataArray.get(randomIndex);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        finally {
            return fakeData;
        }
    }

    public String getRandomFakeZip()
    {
        return String.format("%05d", ThreadLocalRandom.current().nextInt(1000, 100000));
    }

}
