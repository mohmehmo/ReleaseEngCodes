/**
 * 
 * @author MasudRahman
 */

package ca.polymtl.swat.plinteract.sanity;

import java.io.File;
import java.util.HashMap;
import java.util.HashSet;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.parser.Parser;
import org.jsoup.select.Elements;
import utility.ContentLoader;

public class FileOverlapChecker {

	String xmlFolder;
	String javaFolder;
	String cppFolder;

	public FileOverlapChecker(String xmlFolder) {
		this.xmlFolder = xmlFolder;
		this.javaFolder = this.xmlFolder + "-java";
		this.cppFolder = this.xmlFolder + "-cpp";
	}

	protected HashSet<String> extractFunctions(String xmlFile) {
		// extracting the XML elements
		HashSet<String> functionList = new HashSet<String>();
		String xmlContent = ContentLoader.loadFileContent(xmlFile);
		Document doc = Jsoup.parse(xmlContent, "", Parser.xmlParser());
		Elements declarations = doc.select("function");
		for (Element declarationStmt : declarations) {
			// declarationStmt.getElementsByTag("name");
			Elements functions = declarationStmt.select("function > name");
			if (!functions.isEmpty()) {
				for (Element elem : functions) {
					String ccFunctionName = elem.text();
					String[] parts = ccFunctionName.split("::");
					if (parts.length > 1) {
						functionList.add(parts[parts.length-1]);
					}else {
						functionList.add(elem.text());
					}
				}
			}
		}
		return functionList;
	}

	protected HashSet<String> extractFunctionCalls(String xmlFile) {
		// extracting the XML elements
		HashSet<String> functionList = new HashSet<String>();
		String xmlContent = ContentLoader.loadFileContent(xmlFile);
		Document doc = Jsoup.parse(xmlContent, "", Parser.xmlParser());
		Elements declarations = doc.select("expr");
		for (Element declarationStmt : declarations) {
			// declarationStmt.getElementsByTag("name");
			Elements functions = declarationStmt.select("call > name");
			if (!functions.isEmpty()) {
				for (Element elem : functions) {
					functionList.add(elem.text());
				}
			}
		}
		return functionList;
	}

	protected HashSet<String> extractDeclaredFields(String xmlFile) {
		HashSet<String> functionList = new HashSet<String>();
		String xmlContent = ContentLoader.loadFileContent(xmlFile);
		Document doc = Jsoup.parse(xmlContent, "", Parser.xmlParser());
		Elements declarations = doc.select("decl_stmt");
		for (Element declarationStmt : declarations) {
			// declarationStmt.getElementsByTag("name");
			Elements functions = declarationStmt.select("decl > name");
			if (!functions.isEmpty()) {
				for (Element elem : functions) {
					functionList.add(elem.text());
				}
			}
		}
		return functionList;
	}

	protected void determineOverlapLinks(String itemKey) {
		// String itemKey = "F";
		HashMap<String, HashSet<String>> masterJavaList = browseXMLHS(this.javaFolder, itemKey);
		HashMap<String, HashSet<String>> masterCppList = browseXMLHS(this.cppFolder, itemKey);
		for (String key : masterJavaList.keySet()) {
			HashSet<String> temp1 = masterJavaList.get(key);
			for (String ckey : masterCppList.keySet()) {
				HashSet<String> temp2 = masterCppList.get(ckey);
				//temp2.retainAll(temp1);
				boolean flag=false;
				for(String cmethod: temp2) {
					if(temp1.contains(cmethod)) {
						System.out.println(cmethod);
						flag=true;
					}
				}
				
				if (flag) {
					System.out.println(key + "<=>" + ckey);
					//System.out.println(temp2);
				}
			}
		}
	}

	protected void detectOverlaps() {
		HashSet<String> javaMethods = new HashSet<String>();
		HashSet<String> cppMethods = new HashSet<String>();

		javaMethods = browseXML(this.javaFolder);
		cppMethods = browseXML(this.cppFolder);

		System.out.println("Java methods:" + javaMethods.size());
		System.out.println("CPP methods:" + cppMethods.size());

		int common = 0;
		for (String javaMethod : javaMethods) {
			if (cppMethods.contains(javaMethod)) {
				System.out.println(javaMethod);
				common++;
			}
		}

		System.out.println("Common:" + common);

		// determine overlap
		// javaMethods.retainAll(cppMethods);
		// System.out.println(javaMethods);

	}

	protected HashSet<String> browseXML(String targetFolder) {
		File dir = new File(targetFolder);
		File[] files = dir.listFiles();
		HashSet<String> masterList = new HashSet<String>();
		for (File file : files) {
			HashSet<String> temp = extractFunctions(file.getAbsolutePath());
			masterList.addAll(temp);
		}
		return masterList;
	}

	protected HashMap<String, HashSet<String>> browseXMLHS(String targetFolder, String itemKey) {
		File dir = new File(targetFolder);
		File[] files = dir.listFiles();
		HashMap<String, HashSet<String>> masterMap = new HashMap<String, HashSet<String>>();
		for (File file : files) {
			HashSet<String> temp = new HashSet<String>();
			switch (itemKey) {
			case "DS": //declaration statements, mostly fields
				temp = extractDeclaredFields(file.getAbsolutePath());
				break;
			case "F": //function name
				temp = extractFunctions(file.getAbsolutePath());
				break;
			case "FC": //function calls
				temp = extractFunctionCalls(file.getAbsolutePath());
				break;
			default:
				throw new IllegalArgumentException("Unexpected value: " + itemKey);
			}

			if (!temp.isEmpty()) {
				masterMap.put(file.getAbsolutePath(), temp);
			}
		}
		return masterMap;

	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String xmlFolder = "C:\\MyWorks\\SWATLab\\Mehdi\\bitcoin";
		String itemKey = "FC";
		new FileOverlapChecker(xmlFolder).determineOverlapLinks(itemKey);
		//new FileOverlapChecker(xmlFolder).detectOverlaps();
	}
}
