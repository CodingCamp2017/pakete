package com.itestra.codingcamp.androidpost.rest;

import android.os.AsyncTask;

import com.itestra.codingcamp.androidpost.exceptions.InvalidRequestException;
import com.itestra.codingcamp.androidpost.exceptions.InvalidValueException;
import com.itestra.codingcamp.androidpost.exceptions.KeyNotFoundException;
import com.itestra.codingcamp.androidpost.exceptions.NetworkException;
import com.itestra.codingcamp.androidpost.exceptions.ResourceNotFoundException;
import com.itestra.codingcamp.androidpost.exceptions.RestException;
import com.itestra.codingcamp.androidpost.exceptions.ServerException;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by simon on 23.08.17.
 */

public class RestInterface {
    private final String url = "http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8000/";

    public interface ReadyHandler {
        void onReady(AsyncTaskResult result);
    }

    private String convertStreamToString(InputStream is) {
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));
        StringBuilder sb = new StringBuilder();

        String line;
        try {
            while ((line = reader.readLine()) != null) {
                sb.append(line).append('\n');
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                is.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return sb.toString();
    }

    private HttpURLConnection getPostConnection(String urlstring) throws IOException {
        URL url = new URL(urlstring);
        HttpURLConnection httpURLConnection = (HttpURLConnection) url.openConnection();
        httpURLConnection.setDoInput(true);
        httpURLConnection.setDoOutput(true);
        httpURLConnection.setRequestMethod("POST");
        httpURLConnection.setRequestProperty("Content-Type", "application/json");
        return httpURLConnection;
    }

    private JSONObject processResponse(HttpURLConnection connection) throws JSONException, IOException, RestException {
        int statusCode = connection.getResponseCode();

        if (statusCode == 200) {
            BufferedInputStream inputStream = new BufferedInputStream(connection.getInputStream());
            String response = convertStreamToString(inputStream);
            System.out.println("Response: " + response);
            System.out.println("resp msg: " + connection.getResponseMessage());
            return new JSONObject(response);
        } else {
            String errormsg = convertStreamToString(connection.getErrorStream());
            System.out.println("error " + statusCode);
            System.out.println("err stream" + errormsg);

            if (statusCode == 400) {
                JSONObject jsonerror = new JSONObject(errormsg);
                switch (jsonerror.getString("type")) {
                    case "invalid key":
                        throw new InvalidValueException(jsonerror.getString("key"), jsonerror.getString("message"));
                    case "key not found":
                        throw new KeyNotFoundException(jsonerror.getString("key"), jsonerror.getString("message"));
                    case "no data found":
                        throw new InvalidRequestException(jsonerror.getString("message"));
                    default:
                        throw new RestException("unknown error type " + jsonerror.getString("type"));
                }
            } else if (statusCode == 404) {
                throw new ResourceNotFoundException();
            } else if (statusCode == 504) {
                throw new ServerException((new JSONObject(errormsg)).getString("error"));
            } else {
                throw new RestException("Unknown error code: " + statusCode);
            }
        }
    }

    public void sendRequest(String url, Map<String, Object> data, ReadyHandler handler) {
        AsyncTask<Object, Void, AsyncTaskResult> task = (new AsyncTask<Object, Void, AsyncTaskResult>() {
            @Override
            protected AsyncTaskResult doInBackground(Object... params) {
                Map<String, Object> data = (Map<String, Object>)params[0];
                HttpURLConnection connection = null;

                try {
                    connection = getPostConnection(url);

                    JSONObject json = new JSONObject(data);

                    BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(connection.getOutputStream()));
                    bufferedWriter.write(json.toString());
                    bufferedWriter.flush();

                    try {
                        return new AsyncTaskResult(processResponse(connection));
                    } catch (RestException e) {
                        return new AsyncTaskResult(e);
                    } catch (JSONException e) {
                        e.printStackTrace();
                        return new AsyncTaskResult(new RestException("Error parsing JSON: " + e.getMessage()));
                    }
                } catch (IOException e) {
                    return new AsyncTaskResult(new NetworkException("IO EXCEPTION " + e.getMessage()));
                } finally {
                    try {
                        if (connection != null) connection.disconnect();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }

            @Override
            protected void onPostExecute(AsyncTaskResult result) {
                handler.onReady(result);
            }
        }).execute(data);
    }

    public void newPacket(Map<String, Object> data, ReadyHandler handler) {
        sendRequest(RestInterface.this.url + "register", data, handler);
    }

    public void updatePacket(String id, String station, String vehicle, ReadyHandler handler)  {
        Map<String, Object> data = new HashMap<>();
        data.put("station", station);
        data.put("vehicle", vehicle);

        sendRequest(RestInterface.this.url + "packet/" + id +"/update", data, handler);
    }

    public void deliverPacket(String id, ReadyHandler handler) {
        sendRequest(RestInterface.this.url + "packet/" + id +"/delivered", new HashMap<>(), handler);
    }
}