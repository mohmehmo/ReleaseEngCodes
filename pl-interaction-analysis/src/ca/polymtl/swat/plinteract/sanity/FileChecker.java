/**
 * 
 * @author MasudRahman
 */

package ca.polymtl.swat.plinteract.sanity;

import java.io.File;

public class FileChecker {

	String projectFolder;

	public FileChecker(String projectFolder) {
		this.projectFolder = projectFolder;
	}

	protected void collectFileExt() {
		browse(this.projectFolder);
	}

	protected void browse(String folder) {
		File file = new File(folder);
		if (file.isDirectory()) {
			File[] files = file.listFiles();
			for (File f : files) {
				if (f.isDirectory()) {
					browse(f.getAbsolutePath());
				} else {
					if (f.getName().endsWith(".cpp")) {
						System.out.println(f.getName());
					}
					//System.out.println(f.getName());
				}
			}
		} else {
			if (file.getName().endsWith(".cpp")) {
				System.out.println(file.getName());
			}
			//System.out.println(file.getName());
		}

	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String projectFolder = "C:\\MyWorks\\SWATLab\\Mehdi\\Arduino\\app";
		new FileChecker(projectFolder).collectFileExt();

	}
}
