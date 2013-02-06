package org.apache.maven.artifact.repository;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.StringTokenizer;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

public class MavenJPackageDepmap {

    private static class ArtifactDefinition {
        String groupId = null;
        String artifactId = null;
        String version = null;
    }

    /**
     * 
     * @author Stanislav Ochotnicky <sochotnicky@redhat.com>
     * 
     *         This class is used to wrap around fragments that are mapping
     *         artifacts to jar files in our _javadir. These used to be
     *         processed in a macro after every package installation. Fragments
     *         themselves are not proper xml files (they have no root element)
     *         so we have to fix them by wrapping them in one root element.
     */
    private static class WrapFragmentStream extends InputStream {
        String startTag = "<deps>";
        String endTag = "</deps>";
        byte fragmentContent[];
        int position;

        WrapFragmentStream(String fragmentPath) throws IOException {
            FileInputStream fin = new FileInputStream(fragmentPath);
            int nBytes = fin.available();
            byte tmpContent[] = new byte[nBytes];
            fin.read(tmpContent);
            fin.close();
            byte startBytes[] = startTag.getBytes();
            byte endBytes[] = endTag.getBytes();
            fragmentContent = new byte[nBytes + startBytes.length
                    + endBytes.length];
            System.arraycopy(startBytes, 0, fragmentContent, 0,
                    startBytes.length);
            System.arraycopy(tmpContent, 0, fragmentContent, startBytes.length,
                    tmpContent.length);
            System.arraycopy(endBytes, 0, fragmentContent, startBytes.length
                    + tmpContent.length, endBytes.length);
            position = 0;
        }

        public int read() throws IOException {
            if (position < fragmentContent.length) {
                return fragmentContent[position++];
            } else {
                return -1;
            }
        }
    }

    private static MavenJPackageDepmap instance;
    private static Hashtable<String, String> jppArtifactMap;
    private static Hashtable<String, ArrayList<String>> jppUnversionedArtifactMap;

    private MavenJPackageDepmap() {
        jppArtifactMap = new Hashtable<String, String>();
        jppUnversionedArtifactMap = new Hashtable<String, ArrayList<String>>();
        buildJppArtifactMap();
    }

    public static MavenJPackageDepmap getInstance() {
        if (instance == null) {
            instance = new MavenJPackageDepmap();
        }

        return instance;
    }

    /**
     * This function can be used to query exact version of an artifact.
     * 
     * @param groupId
     * @param artifactId
     * @param version
     * @return Hashtable mapping for groupId, artifactId and version or null if
     *         exact mapping not found
     */
    public Hashtable<String, String> getMappedInfo(String groupId,
            String artifactId, String version) {

        Hashtable<String, String> jppDep;
        String idToCheck, jppCombination;

        idToCheck = groupId + "," + artifactId + "," + version;

        jppCombination = (String) jppArtifactMap.get(idToCheck);
        jppDep = null;
        if (jppCombination != null && jppCombination != "") {
            StringTokenizer st = new StringTokenizer(jppCombination, ",");
            jppDep = new Hashtable<String, String>();
            jppDep.put("group", st.nextToken());
            jppDep.put("artifact", st.nextToken());
            jppDep.put("version", st.nextToken());

        }

        return jppDep;
    }

    /**
     * This function can be used to query for all possible artifact resolutions.
     * It works with multiple duplicate gid:aid mappings, but only one should
     * have unversioned files (default version) to work properly later
     * 
     * @param groupId
     * @param artifactId
     * @param version
     * @return
     */
    public ArrayList<Hashtable<String, String>> getUnversionedMappedInfo(
            String groupId, String artifactId, String version) {

        Hashtable<String, String> jppDep;
        String idToCheck;
        List<String> maps;

        idToCheck = groupId + "," + artifactId;

        maps = jppUnversionedArtifactMap.get(idToCheck);
        ArrayList<Hashtable<String, String>> ret = new ArrayList<Hashtable<String, String>>();
        if (maps != null) {
            for (String jppPart : maps) {
                jppDep = new Hashtable<String, String>();
                StringTokenizer st = new StringTokenizer(jppPart, ",");

                jppDep.put("group", st.nextToken());
                jppDep.put("artifact", st.nextToken());
                jppDep.put("version", st.nextToken());

                // we add to index 0 to make it reversed order for compatibility
                // with older code
                ret.add(0, jppDep);
            }
        }
        return ret;
    }

    private static void buildJppArtifactMap() {

        processDepmapFile("/etc/maven/maven2-versionless-depmap.xml");

        // process fragments in etc
        File fragmentDir = new File("/etc/maven/fragments");
        String flist[] = fragmentDir.list();
        if (flist != null) {
            java.util.Arrays.sort(flist);
            for (String fragFilename : flist)
                processDepmapFile("/etc/maven/fragments/" + fragFilename);
        }

        // process fragments is usr. Once packages are rebuilt, we can skip
        // fragments in /etc
        fragmentDir = new File("/usr/share/maven-fragments");
        flist = fragmentDir.list();
        if (flist != null) {
            java.util.Arrays.sort(flist);
            for (String fragFilename : flist)
                processDepmapFile("/usr/share/maven-fragments/" + fragFilename);
        }

        String customDepmapDir = System.getProperty("maven.local.depmap.dir",
                null);
        if (customDepmapDir != null) {
            fragmentDir = new File(customDepmapDir);
            flist = fragmentDir.list();
            if (flist != null) {
                java.util.Arrays.sort(flist);
                for (String fragFilename : flist)
                    processDepmapFile(customDepmapDir + File.separator
                            + fragFilename);
            }
        }

        String customFileName = System.getProperty("maven.local.depmap.file",
                null);
        if (customFileName != null) {
            processDepmapFile(customFileName);
        }

    }

    private static void processDepmapFile(String fileName) {

        Document mapDocument;
        debug("Loading depmap file: " + fileName);
        try {
            DocumentBuilderFactory fact = DocumentBuilderFactory.newInstance();
            fact.setNamespaceAware(true);
            DocumentBuilder builder = fact.newDocumentBuilder();
            // we can wrap even old depmaps, no harm done
            WrapFragmentStream wfs = new WrapFragmentStream(fileName);
            mapDocument = builder.parse(wfs);
            wfs.close();
        } catch (FileNotFoundException fnfe) {
            System.err.println("ERROR: Unable to find map file: " + fileName);
            fnfe.printStackTrace();
            return;
        } catch (IOException ioe) {
            System.err
                    .println("ERROR: I/O exception occured when opening map file");
            ioe.printStackTrace();
            return;
        } catch (ParserConfigurationException pce) {
            System.err
                    .println("ERROR: Parsing of depmap file failed - configuration");
            pce.printStackTrace();
            return;
        } catch (SAXException se) {
            System.err.println("ERROR: Parsing of depmap file failed");
            se.printStackTrace();
            return;
        }

        NodeList depNodes = (NodeList) mapDocument
                .getElementsByTagName("dependency");

        for (int i = 0; i < depNodes.getLength(); i++) {
            Element depNode = (Element) depNodes.item(i);

            NodeList mavenNodeList = (NodeList) depNode
                    .getElementsByTagName("maven");
            if (mavenNodeList.getLength() != 1) {
                debug("Number of maven sub-elements is not 1. Bailing from depmap generation");
                debug("Maven node: " + depNode.getTextContent());
                return;
            }
            ArtifactDefinition mavenAD = getArtifactDefinition((Element) mavenNodeList
                    .item(0));

            ArtifactDefinition jppAD = null;
            NodeList jppNodeList = (NodeList) depNode
                    .getElementsByTagName("jpp");

            if (jppNodeList.getLength() == 1) {
                jppAD = getArtifactDefinition((Element) jppNodeList.item(0));
                debug("*** Adding: " + mavenAD.groupId + ","
                        + mavenAD.artifactId + " => " + jppAD.groupId + ","
                        + jppAD.artifactId + "," + jppAD.version + " to map...");

                jppArtifactMap.put(mavenAD.groupId + "," + mavenAD.artifactId
                        + "," + mavenAD.version, jppAD.groupId + ","
                        + jppAD.artifactId + "," + jppAD.version);
                ArrayList<String> maps = jppUnversionedArtifactMap
                        .get(mavenAD.groupId + "," + mavenAD.artifactId);
                if (maps == null) {
                    maps = new ArrayList<String>();
                }

                maps.add(jppAD.groupId + "," + jppAD.artifactId + ","
                        + jppAD.version);

                jppUnversionedArtifactMap.put(mavenAD.groupId + ","
                        + mavenAD.artifactId, maps);
            } else {
                debug("Number of jpp sub-elements is not 1. Dropping dependency for "
                        + mavenAD.groupId + ":" + mavenAD.artifactId);
                jppArtifactMap.put(mavenAD.groupId + "," + mavenAD.artifactId
                        + "," + mavenAD.version, "JPP/maven,empty-dep,"
                        + mavenAD.version);
                ArrayList<String> maps = new ArrayList<String>();
                maps.add("JPP/maven,empty-dep," + mavenAD.version);
                jppUnversionedArtifactMap.put(mavenAD.groupId + ","
                        + mavenAD.artifactId, maps);
            }
        }
    }

    private static ArtifactDefinition getArtifactDefinition(Element element) {
        ArtifactDefinition ad = new ArtifactDefinition();

        NodeList nodes = element.getElementsByTagName("groupId");
        if (nodes.getLength() != 1) {
            debug("groupId definition not found in depmap");
            return null;
        }
        ad.groupId = nodes.item(0).getTextContent();

        nodes = element.getElementsByTagName("artifactId");
        if (nodes.getLength() != 1) {
            debug("artifactId definition not found in depmap");
            return null;
        }
        ad.artifactId = nodes.item(0).getTextContent();

        nodes = element.getElementsByTagName("version");
        if (nodes.getLength() != 1) {
            ad.version = "DUMMY_VER";
        } else {
            ad.version = nodes.item(0).getTextContent();
        }
        return ad;
    }

    public static void debug(String msg) {
        if (System.getProperty("maven.local.debug") != null)
            System.err.println(msg);
    }
}
