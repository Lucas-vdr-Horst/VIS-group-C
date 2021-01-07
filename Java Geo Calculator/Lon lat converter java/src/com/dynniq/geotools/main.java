//Copyright (c) 2017, Dynniq (www.dynniq.com)
//All rights reserved.
//
//Redistribution and use in source and binary forms, with or without
//modification, are permitted provided that the following conditions are met:
//
//1. Redistributions of source code must retain the above copyright notice, this
// list of conditions and the following disclaimer.
//2. Redistributions in binary form must reproduce the above copyright notice,
// this list of conditions and the following disclaimer in the documentation
// and/or other materials provided with the distribution.
//
//THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
//ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
//WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
//DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
//ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
//(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
//LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
//ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
//(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
//SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
package com.dynniq.geotools;
import java.text.DecimalFormat;
/**
 * Class dealing with WGS84 locations
 *
 * @author eckoende (Eric Koenders, Dynniq)
 *
 */
class GeoPoint {
    private double lon;
    private double lat;
    private static DecimalFormat df = new DecimalFormat("#.######");

    public GeoPoint(double lon, double lat) {
        this.lon = lon;
        this.lat = lat;
    }

    public double getLon() {
        return lon;
    }

    public void setLon(double lon) {
        this.lon = lon;
    }

    public double getLat() {
        return lat;
    }

    public void setLat(double lat) {
        this.lat = lat;
    }

    public GeoPoint clone() {
        return new GeoPoint(lon, lat);
    }

    public final static double EarthRadius = 6367000.0; // in meters

    /**
     * Calculate the distance between two points in meters.
     * <p>
     * <p>
     * Annex B: Conversion code absolute – relative positions 49
     *
     * @param other the other GeoPoint
     * @return the geographic distance between this point and the other in meters
     */
    public double geodistance(GeoPoint other) {
// convert to radians
        double lon1 = Math.toRadians(this.lon);
        double lat1 = Math.toRadians(this.lat);
        double lon2 = Math.toRadians(other.lon);
        double lat2 = Math.toRadians(other.lat);
// Haversine formula
        double dlon = lon2 - lon1;
        double dlat = lat2 - lat1;
        double a = haversin(dlat) + Math.cos(lat1) * Math.cos(lat2) * haversin(dlon);
        return EarthRadius * haverasin(a);
    }

    /**
     * Calculate the longitude difference between two point in meters.
     * A negative value is returned if the other point is to the west.
     *
     * @param other the other GeoPoint
     * @return the geographic distance between this point and the other in meters
     */
    public double geodistance_lon(GeoPoint other) {
// convert to radians
        double lon1 = Math.toRadians(this.lon);
        double lat1 = Math.toRadians(this.lat);
        double lon2 = Math.toRadians(other.lon);
// Haversine formula
        double dlon = lon1 - lon2;
        double a = Math.cos(lat1) * Math.cos(lat1) * haversin(dlon);
        return EarthRadius * haverasin(a) * (dlon < 0 ? -1 : 1);
    }

    /**
     * Calculate the latitude difference between two point in meters.
     * A negative value is returned if the other point is to the south.
     *
     * @param other the other GeoPoint
     * @return the geographic distance between this point and the other in meters
     */
    public double geodistance_lat(GeoPoint other) {
// convert to radians
        double lat1 = Math.toRadians(this.lat);
        double lat2 = Math.toRadians(other.lat);
// Haversine formula
        double dlat = lat1 - lat2;
        double a = haversin(dlat);
        return EarthRadius * haverasin(a) * (dlat < 0 ? -1 : 1);
    }

    /**
     * @param distance The distance to offset the longitude in meters
     * @brief Move the longitude by the given distance
     * A negative value must be used when moving to the west.
     */
    public void geodisplace_lon(double distance) {
        double reflat = Math.toRadians(this.lat);
        double reflon = Math.toRadians(this.lon);
        double cosreflat = Math.cos(reflat);
        double dlon = haverasin(haversin(distance / EarthRadius) / cosreflat / cosreflat);
        if (distance < 0)
            this.lon = Math.toDegrees(reflon - dlon);
        else
            this.lon = Math.toDegrees(reflon + dlon);
    }

    /**
     * @param distance The distance to offset the latitude in meters
     * @brief Move the latitude by the given distance
     * A negative value must be used when moving to the south.
     */
    public void geodisplace_lat(double distance) {
        double reflat = Math.toRadians(this.lat);
        double dlat = distance / EarthRadius;
        this.lat = Math.toDegrees(reflat + dlat);
    }

    /**
     * Haversine formula, see https://en.wikipedia.org/wiki/Haversine_formula
     *
     * @param a
     * @return the haversine of a
     */
    public static double haversin(double a) {
        return Math.pow(Math.sin(a / 2), 2);
    }

    /**
     * Inverse Haversine formula, see https://en.wikipedia.org/wiki/Haversine_formula
     *
     * @param a
     * @return the haverasine of a
     */
    public static double haverasin(double a) {
        return 2 * Math.asin(Math.min(1, Math.sqrt(a)));
    }

    public String toString() {
        return "[" + df.format(lon) + "," + df.format(lat) + "] ";
    }

    public static void main(String args[]) {

        double lon1 = 52943788  / 10000000.0;
        double lat1 = 516829984 / 10000000.0;

        double lon2 = 52939548 / 10000000.0;
        double lat2 = 516831515 / 10000000.0;

        System.out.println(lon1);
        /* take a reference location */
        GeoPoint refloc = new GeoPoint( lon1 , lat1);
        /* take a point */
        GeoPoint pnt = new GeoPoint(lon2 , lat2 );
        /* calculate the delta differences */

        double deltax = pnt.geodistance_lon(refloc);
        double deltay = pnt.geodistance_lat(refloc);
        System.out.println("Refloc = " + refloc);
        System.out.println("Point = " + pnt + " delta [x,y] = [" + deltax + ", " + deltay + "]");
        /* take a point at the reference location */
        GeoPoint node = refloc.clone();
        /* move the point by a delta */
        node.geodisplace_lon(deltax);
        node.geodisplace_lat(deltay);
        System.out.println("Node = " + node);
    }
}