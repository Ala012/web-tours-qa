import jenkins.model.Jenkins

import java.io.ByteArrayInputStream
import java.io.StringReader
import java.nio.charset.StandardCharsets
import java.nio.file.Files
import java.nio.file.Paths
import javax.xml.transform.stream.StreamSource

// Cree (ou met a jour) le job WebTours-QA depuis le XML monte en lecture seule.
def name = 'WebTours-QA'
def configPath = '/opt/jenkins-config/WebTours-QA.xml'
def jenkins = Jenkins.get()

def path = Paths.get(configPath)
if (!Files.exists(path)) {
    println "[init] Config du job absente : ${configPath}"
    return
}

def xml = Files.readString(path, StandardCharsets.UTF_8)
def job = jenkins.getItem(name)

if (job == null) {
    jenkins.createProjectFromXML(name, new ByteArrayInputStream(xml.getBytes(StandardCharsets.UTF_8)))
    println "[init] Job ${name} cree"
} else {
    job.updateByXml(new StreamSource(new StringReader(xml)))
    println "[init] Job ${name} mis a jour"
}
jenkins.save()
