/**
 * 
 * @author MasudRahman
 */

package ca.polymtl.swat.plinteract.sanity;

import java.io.File;
import java.nio.file.Files;

public class DataSeparator {

	String homeFolder;
	String javaFolder;
	String cppFolder;

	public DataSeparator(String homeFolder) {
		this.homeFolder = homeFolder;
		this.javaFolder = this.homeFolder + "-java";
		makeFolder(this.javaFolder);
		this.cppFolder = this.homeFolder + "-cpp";
		makeFolder(this.cppFolder);
	}

	protected void makeFolder(String targetFolder) {
		File dir = new File(targetFolder);
		if (!dir.exists()) {
			dir.mkdir();
		}
	}

	protected void separateDataset() {
		File dir = new File(this.homeFolder);
		if (dir.isDirectory()) {
			File[] files = dir.listFiles();
			for (File f : files) {
				try {
					String fileName = f.getName();
					if (fileName.contains("_java_")) {
						String targetFile = this.javaFolder + "\\" + f.getName();
						Files.copy(f.toPath(), new File(targetFile).toPath());
					} else if (fileName.contains("_h_") || fileName.contains("_cpp_")) {
						String targetFile = this.cppFolder + "\\" + f.getName();
						Files.copy(f.toPath(), new File(targetFile).toPath());
					}
				} catch (Exception exc) {
					// handle the exception
					exc.printStackTrace();
					System.exit(1);
				}
			}
		}
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String homeFolder = "C:\\MyWorks\\SWATLab\\Mehdi\\netdata";
		new DataSeparator(homeFolder).separateDataset();
	}

}
