package com.itestra.codingcamp.androidpost.rest;

import android.os.AsyncTask;

import com.itestra.codingcamp.androidpost.exceptions.InvalidRequestException;
import com.itestra.codingcamp.androidpost.exceptions.InvalidValueException;
import com.itestra.codingcamp.androidpost.exceptions.KeyNotFoundException;
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
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.concurrent.ExecutionException;

/**
 * Created by simon on 23.08.17.
 */

public class RestInterface {
    private final String url = "http://ec2-35-158-239-16.eu-central-1.compute.amazonaws.com:8000/";

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

    private JSONObject handleResponse(HttpURLConnection connection) throws JSONException, IOException, RestException {
        int statusCode = connection.getResponseCode();

        System.out.println("Status: " + statusCode);

        if (statusCode == 200) {
            BufferedInputStream inputStream = new BufferedInputStream(connection.getInputStream());
            String response = convertStreamToString(inputStream);
            System.out.println("Response: " + response);
            System.out.println("resp msg" + connection.getResponseMessage());
            return new JSONObject(response);
        } else {
            String errormsg = convertStreamToString(connection.getErrorStream());
            System.out.println("error " + statusCode);
            System.out.println("err stream" + errormsg);

            if (statusCode == 400) {
                JSONObject jsonerror = new JSONObject(errormsg);
                switch (jsonerror.getString("type")) {
                    case "invalid key": throw new InvalidValueException(jsonerror.getString("key"), jsonerror.getString("message"));
                    case "key not found": throw new KeyNotFoundException(jsonerror.getString("key"), jsonerror.getString("message"));
                    case "no data found": throw new InvalidRequestException(jsonerror.getString("message"));
                    default: throw new RestException("unknown error type " + jsonerror.getString("type"));
                }
            } else if (statusCode == 504) {
                throw new ServerException((new JSONObject(errormsg)).getString("error"));
            } else {
                throw new RestException("Unknown error code: " + statusCode);
            }
        }
    }

    public String newPackage(HashMap<String, String> data) throws ExecutionException, InterruptedException, RestException {
        AsyncTaskResult<String> result = (new AsyncTask<Object, Void, AsyncTaskResult<String>>() {
            @Override
            protected AsyncTaskResult<String> doInBackground(Object... params) {
                HashMap<String, String> data = (HashMap<String, String>)params[0];
                HttpURLConnection connection = null;

                try {
                    connection = getPostConnection(RestInterface.this.url + "register");

                    JSONObject json = new JSONObject();
                    try {
                        for (String key : data.keySet()) {
                            json.put(key, data.get(key));
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                    BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(connection.getOutputStream()));
                    bufferedWriter.write(json.toString());
                    bufferedWriter.flush();

                    System.out.println(json.toString());
                    try {
                        JSONObject response = handleResponse(connection);
                        return new AsyncTaskResult<String>(response.getString("id"));
                    } catch (RestException e) {
                        return new AsyncTaskResult<String>(e);
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                } catch (JSONException e) {
                    e.printStackTrace();
                } finally {
                    try {
                        if (connection != null) connection.disconnect();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
                return null;
            }
        }).execute(data).get();

        if (result.hasError()) {
            throw result.getError();
        } else {
            return result.getResult();
        }
    }

    public void updatePackage(String id, String station, String vehicle) {
        (new AsyncTask<String, Void, Void>() {
            @Override
            protected Void doInBackground(String... params) {
                String id = params[0];
                String station = params[1];
                String vehicle = params[2];

                System.out.println("update package with ID: " + id + "(" + station + ", " + vehicle + ")");

                OutputStream outputStream = null;
                BufferedInputStream inputStream = null;

                try {
                    HttpURLConnection connection = getPostConnection(RestInterface.this.url + "packet/" + id +"/update");

                    outputStream = connection.getOutputStream();

                    JSONObject json = new JSONObject();
                    try {
                        json.put("station", station);
                        json.put("vehicle", vehicle);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                    BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(outputStream));
                    bufferedWriter.write(json.toString());
                    bufferedWriter.flush();

                    System.out.println(json.toString());

                    int statusCode = connection.getResponseCode();

                    System.out.println("Status: " + statusCode);

                    if (statusCode == 200) {
                        inputStream = new BufferedInputStream(connection.getInputStream());
                        String response = convertStreamToString(inputStream);
                        System.out.println("Response: " + response);
                        System.out.println("resp msg" + connection.getResponseMessage());
                    } else {
                        System.out.println("error " + statusCode);
                        System.out.println("err stream" + convertStreamToString(connection.getErrorStream()));
                    }

                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    try {
                        if (inputStream != null) inputStream.close();
                        if (outputStream != null) outputStream.close();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
                return null;
            }
        }).execute(id, station, vehicle);
    }

    public void deliverPacket(String id) {
        (new AsyncTask<String, Void, Void>() {
            @Override
            protected Void doInBackground(String... params) {
                String id = params[0];

                System.out.println("deliver package with ID: " + id);

                OutputStream outputStream = null;
                BufferedInputStream inputStream = null;

                try {
                    HttpURLConnection connection = getPostConnection(RestInterface.this.url + "packet/" + id +"/delivered");

                    outputStream = connection.getOutputStream();

                    BufferedWriter bufferedWriter = new BufferedWriter(new OutputStreamWriter(outputStream));
                    bufferedWriter.write("{}");
                    bufferedWriter.flush();

                    int statusCode = connection.getResponseCode();

                    System.out.println("Status: " + statusCode);

                    if (statusCode == 200) {
                        inputStream = new BufferedInputStream(connection.getInputStream());
                        String response = convertStreamToString(inputStream);
                        System.out.println("Response: " + response);
                        System.out.println("resp msg" + connection.getResponseMessage());
                    } else {
                        System.out.println("error " + statusCode);
                        System.out.println("err stream" + convertStreamToString(connection.getErrorStream()));
                    }

                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    try {
                        if (inputStream != null) inputStream.close();
                        if (outputStream != null) outputStream.close();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
                return null;
            }
        }).execute(id);
    }
}