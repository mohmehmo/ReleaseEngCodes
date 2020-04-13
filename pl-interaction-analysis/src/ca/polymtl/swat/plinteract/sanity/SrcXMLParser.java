
/**
 * 
 * @author MasudRahman
 */

package ca.polymtl.swat.plinteract.sanity;

import java.io.File;
import java.util.HashSet;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.parser.Parser;
import org.jsoup.select.Elements;
import utility.ContentLoader;

public class SrcXMLParser {

	String xmlFolder;
	String javaFolder;
	String cppFolder;

	public SrcXMLParser(String xmlFolder) {
		this.xmlFolder = xmlFolder;
		this.javaFolder = this.xmlFolder + "-java";
		this.cppFolder = this.xmlFolder + "-cpp";
	}

	protected HashSet<String> extractMethodInvocations(String xmlFile) {
		String xmlContent = ContentLoader.loadFileContent(xmlFile);
		HashSet<String> calls = new HashSet<String>();
		Document doc = Jsoup.parse(xmlContent, "", Parser.xmlParser());
		Elements declarations = doc.getElementsByTag("cpp:define");
		for (Element declaration : declarations) {
			//Element macro = declaration.getElementsByTag("name").first();
			//calls.add(macro.text());
			System.out.println(declaration.text());
		}
		return calls;
	}

	protected void detectOverlappingCalls() {
		File[] javaFiles = new File(this.javaFolder).listFiles();
		File[] cppFiles = new File(this.cppFolder).listFiles();
		HashSet<String> javaMethods = new HashSet<String>();
		HashSet<String> cppMethods = new HashSet<String>();
		/*
		 * for (File f : javaFiles) { HashSet<String> temp1 =
		 * extractMethodInvocations(f.getAbsolutePath()); if (!temp1.isEmpty()) {
		 * javaMethods.addAll(temp1); } }
		 */
		
		//System.out.println("Total Java methods:"+javaMethods.size());
		//System.out.println(javaMethods);

		for (File f : cppFiles) {
			HashSet<String> temp1 = extractMethodInvocations(f.getAbsolutePath());
			if (!temp1.isEmpty()) {
				cppMethods.addAll(temp1);
			}
		}
		
		System.out.println("Total CPP methods:"+cppMethods.size());
		System.out.println(cppMethods.contains("JNIEXPORT"));
		System.out.println(cppMethods.contains("JNIMPORT"));
		System.out.println(cppMethods.contains("JNICALL"));
		
		//javaMethods.retainAll(cppMethods);

		System.out.println(javaMethods);

	}

	protected void extractXML(String xmlFile) {
		// extracting the XML elements
		String xmlContent = ContentLoader.loadFileContent(xmlFile);
		Document doc = Jsoup.parse(xmlContent, "", Parser.xmlParser());
		Elements declarations = doc.select("decl_stmt");
		for (Element declarationStmt : declarations) {
			Elements specifiers = declarationStmt.select("call");
			if (!specifiers.isEmpty()) {
				for (Element specifier : specifiers) {
					String specName = specifier.text().trim();
					if (specName.equals("call")) {
						System.out.println(declarationStmt.text());
					}
				}
			}
		}
	}

	protected void browseXML() {
		File dir = new File(this.xmlFolder);
		File[] files = dir.listFiles();
		for (File file : files) {
			extractXML(file.getAbsolutePath());
		}
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String xmlFolder = "C:\\MyWorks\\SWATLab\\Mehdi\\Arduino-XML";
		new SrcXMLParser(xmlFolder).detectOverlappingCalls();
	}
}
