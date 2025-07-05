// DYMO Label Printer Extension
class DymoLabelPrinter {
    constructor() {
        this.labelTypes = [];
        this.dymoConnect = null;
        this.labelXml = null;
        this.init();
    }

    async init() {
        console.log('DymoLabelPrinter: Initializing...');
        await this.loadLabelTypes();
        await this.loadLabelTemplate();
        this.setupEventListeners();
        this.populateDropdown();
        console.log('DymoLabelPrinter: Initialization complete');
    }

    async loadLabelTypes() {
        try {
            const result = await chrome.storage.local.get(['labelTypes']);
            this.labelTypes = result.labelTypes || ['CPU', 'MOBO', 'Screen'];
            console.log('Loaded label types:', this.labelTypes);
        } catch (error) {
            console.error('Error loading label types:', error);
            this.labelTypes = ['CPU', 'MOBO', 'Screen'];
        }
    }

    async saveLabelTypes() {
        try {
            await chrome.storage.local.set({ labelTypes: this.labelTypes });
            console.log('Saved label types:', this.labelTypes);
        } catch (error) {
            console.error('Error saving label types:', error);
        }
    }

    async loadLabelTemplate() {
        // Load the label template from the extension
        this.labelXml = `<?xml version="1.0" encoding="utf-8"?>
<DieCutLabel Version="8.0" Units="twips" MediaType="Default">
  <PaperOrientation>Landscape</PaperOrientation>
  <Id>Address</Id>
  <PaperName>30252 Address</PaperName>
  <DrawCommands>
    <RoundRectangle X="0" Y="0" Width="1581" Height="5040" Rx="270" Ry="270"/>
  </DrawCommands>
  <ObjectInfo>
    <BarcodeObject>
      <Name>Barcode</Name>
      <ForeColor Alpha="255" Red="0" Green="0" Blue="0"/>
      <BackColor Alpha="0" Red="255" Green="255" Blue="255"/>
      <LinkedObjectName></LinkedObjectName>
      <Rotation>Rotation0</Rotation>
      <IsMirrored>False</IsMirrored>
      <IsVariable>True</IsVariable>
      <Text>{{SKU}}</Text>
      <Type>Code128A</Type>
      <Size>Small</Size>
      <TextPosition>Bottom</TextPosition>
      <TextFont Family="Arial" Size="9" Bold="False" Italic="False" Underline="False" Strikeout="False"/>
      <CheckSumFont Family="Arial" Size="7.3125" Bold="False" Italic="False" Underline="False" Strikeout="False"/>
      <TextEmbedding>None</TextEmbedding>
      <ECLevel>0</ECLevel>
      <HorizontalAlignment>Center</HorizontalAlignment>
      <QuietZonesPadding Left="0" Right="0" Top="0" Bottom="0"/>
    </BarcodeObject>
    <Bounds X="331.2" Y="680.3149" Width="4440.473" Height="765.7087"/>
  </ObjectInfo>
  <ObjectInfo>
    <TextObject>
      <Name>Text</Name>
      <ForeColor Alpha="255" Red="0" Green="0" Blue="0"/>
      <BackColor Alpha="0" Red="255" Green="255" Blue="255"/>
      <LinkedObjectName></LinkedObjectName>
      <Rotation>Rotation0</Rotation>
      <IsMirrored>False</IsMirrored>
      <IsVariable>True</IsVariable>
      <HorizontalAlignment>Center</HorizontalAlignment>
      <VerticalAlignment>Top</VerticalAlignment>
      <TextFitMode>ShrinkToFit</TextFitMode>
      <UseFullFontHeight>True</UseFullFontHeight>
      <Verticalized>False</Verticalized>
      <StyledText>
        <Element>
          <String>{{LABEL_TYPE}}</String>
          <Attributes>
            <Font Family="Arial" Size="12" Bold="False" Italic="False" Underline="False" Strikeout="False"/>
            <ForeColor Alpha="255" Red="0" Green="0" Blue="0"/>
          </Attributes>
        </Element>
      </StyledText>
    </TextObject>
    <Bounds X="331" Y="163" Width="4442" Height="341.5669"/>
  </ObjectInfo>
</DieCutLabel>`;
        console.log('Label template loaded');
    }

    setupEventListeners() {
        const labelTypeSelect = document.getElementById('labelType');
        const addNewContainer = document.getElementById('addNewContainer');
        const newLabelTypeInput = document.getElementById('newLabelType');
        const saveNewLabelBtn = document.getElementById('saveNewLabel');
        const cancelNewLabelBtn = document.getElementById('cancelNewLabel');
        const printLabelBtn = document.getElementById('printLabel');

        labelTypeSelect.addEventListener('change', (e) => {
            if (e.target.value === 'add-new') {
                addNewContainer.style.display = 'block';
                newLabelTypeInput.focus();
            } else {
                addNewContainer.style.display = 'none';
            }
        });

        saveNewLabelBtn.addEventListener('click', () => this.saveNewLabelType());
        cancelNewLabelBtn.addEventListener('click', () => this.cancelNewLabelType());
        printLabelBtn.addEventListener('click', () => {
            console.log('Print button clicked');
            this.printLabel();
        });

        // Handle Enter key in new label input
        newLabelTypeInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.saveNewLabelType();
            }
        });

        // Handle Enter key in SKU input
        document.getElementById('sku').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                console.log('Enter pressed in SKU field');
                this.printLabel();
            }
        });
    }

    populateDropdown() {
        const select = document.getElementById('labelType');
        // Clear existing options except the first and last
        while (select.children.length > 2) {
            select.removeChild(select.children[1]);
        }

        // Add label types
        this.labelTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            select.insertBefore(option, select.lastElementChild);
        });
        console.log('Dropdown populated with:', this.labelTypes);
    }

    async saveNewLabelType() {
        const input = document.getElementById('newLabelType');
        const newType = input.value.trim().toUpperCase();
        
        if (!newType) {
            this.showStatus('Please enter a label type', 'error');
            return;
        }

        if (this.labelTypes.includes(newType)) {
            this.showStatus('Label type already exists', 'error');
            return;
        }

        this.labelTypes.push(newType);
        await this.saveLabelTypes();
        this.populateDropdown();
        
        // Select the new label type
        document.getElementById('labelType').value = newType;
        this.cancelNewLabelType();
        
        this.showStatus('Label type added successfully', 'success');
    }

    cancelNewLabelType() {
        document.getElementById('addNewContainer').style.display = 'none';
        document.getElementById('newLabelType').value = '';
        document.getElementById('labelType').value = '';
    }

    async printLabel() {
        console.log('printLabel() called');
        
        const labelType = document.getElementById('labelType').value;
        const sku = document.getElementById('sku').value.trim();

        console.log('Label type:', labelType);
        console.log('SKU:', sku);

        if (!labelType || labelType === 'add-new') {
            console.log('No label type selected');
            this.showStatus('Please select a label type', 'error');
            return;
        }

        if (!sku) {
            console.log('No SKU entered');
            this.showStatus('Please enter a SKU', 'error');
            return;
        }

        try {
            console.log('Checking DYMO Connect...');
            this.showStatus('Connecting to DYMO Connect...', 'success');
            
            await this.initializeDymoConnect();
            console.log('DYMO Connect OK, printing...');
            
            this.showStatus('Printing label...', 'success');
            await this.printLabelWithDymo(labelType, sku);
            
        } catch (error) {
            console.error('Print error:', error);
            this.showStatus(`Print failed: ${error.message}`, 'error');
        }
    }

    async initializeDymoConnect() {
        console.log('Checking DYMO Connect status...');
        
        try {
            const response = await fetch('https://127.0.0.1:41951/DYMO/DLS/Printing/StatusConnected', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            console.log('DYMO Connect response:', response.status, response.statusText);
            
            if (!response.ok) {
                throw new Error(`DYMO Connect not available (${response.status})`);
            }
            
            const status = await response.text();
            console.log('DYMO Connect status:', status);
            
            if (status.trim() !== 'true') {
                throw new Error('DYMO Connect is not ready');
            }
            
            return true;
        } catch (error) {
            console.error('DYMO Connect check failed:', error);
            throw new Error(`DYMO Connect is not running or not accessible: ${error.message}`);
        }
    }

    async printLabelWithDymo(labelType, sku) {
        console.log('Preparing to print with DYMO...');
        
        // Replace placeholders in the label XML
        let labelXml = this.labelXml.replace('{{LABEL_TYPE}}', labelType);
        labelXml = labelXml.replace('{{SKU}}', sku);
        
        console.log('Label XML prepared');
        console.log('Label XML preview:', labelXml.substring(0, 200) + '...');

        try {
            // Get available printers
            console.log('Getting printers...');
            const printersResponse = await fetch('https://127.0.0.1:41951/DYMO/DLS/Printing/GetPrinters', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            console.log('Printers response:', printersResponse.status, printersResponse.statusText);
            
            if (!printersResponse.ok) {
                throw new Error(`Failed to get printers (${printersResponse.status})`);
            }
            
            const printers = await printersResponse.text();
            console.log('Printers XML:', printers);
            
            // Check if we have an empty printers response
            if (!printers || printers.trim() === '<?xml version="1.0" encoding="utf-8"?>\n<Printers/>' || printers.includes('<Printers/>')) {
                console.log('No printers detected by DYMO Connect API');
                throw new Error('No DYMO printers detected. Please check:\n\n1. Power cycle your printer (unplug for 20 seconds)\n2. Make sure printer is connected directly to computer (not via USB hub)\n3. Check that printer appears in System Preferences > Printers\n4. Try restarting DYMO Connect\n5. Test printing from DYMO Connect app first\n\nIf your printer works in DYMO Connect app but not here, try printing without specifying a printer name.');
            }

            // Parse printers XML to get first available printer
            const parser = new DOMParser();
            const printersDoc = parser.parseFromString(printers, 'text/xml');
            
            // Try different possible element names
            let printerElements = printersDoc.getElementsByTagName('LabelWriterPrinter');
            if (printerElements.length === 0) {
                printerElements = printersDoc.getElementsByTagName('Printer');
            }
            if (printerElements.length === 0) {
                printerElements = printersDoc.getElementsByTagName('DYMOPrinter');
            }
            
            console.log('Found printer elements:', printerElements.length);
            
            if (printerElements.length === 0) {
                // Try to print without specifying a printer (use default)
                console.log('No specific printer found, attempting to print to default printer');
                return await this.printWithoutSpecifyingPrinter(labelXml, labelType, sku);
            }

            const printerName = printerElements[0].getAttribute('Name') || printerElements[0].getAttribute('name') || printerElements[0].textContent;
            console.log('Using printer:', printerName);

            // Print the label
            console.log('Sending print request...');
            const printResult = await this.sendPrintRequest(printerName, labelXml, labelType, sku);
            
        } catch (error) {
            console.error('Print with DYMO failed:', error);
            throw error;
        }
    }

    async printWithoutSpecifyingPrinter(labelXml, labelType, sku) {
        console.log('Attempting to print without specifying printer name...');
        return await this.sendPrintRequest('', labelXml, labelType, sku);
    }

    async sendPrintRequest(printerName, labelXml, labelType, sku) {
        console.log('Sending print request with printer:', printerName || 'default');
        
        // Manually build the URL-encoded form data to avoid double-encoding
        const formData = [
            `printerName=${encodeURIComponent(printerName)}`,
            `printParamsXml=${encodeURIComponent('')}`,
            `labelXml=${encodeURIComponent(labelXml)}`,
            `labelSetXml=${encodeURIComponent('')}`
        ].join('&');

        console.log('Form data length:', formData.length);

        const printResponse = await fetch('https://127.0.0.1:41951/DYMO/DLS/Printing/PrintLabel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        console.log('Print response:', printResponse.status, printResponse.statusText);

        if (!printResponse.ok) {
            const errorText = await printResponse.text();
            console.error('Print error response:', errorText);
            
            if (errorText.includes('Invalid parameter in stream') || errorText.includes('labelXml')) {
                throw new Error(`Print failed: XML formatting error. Please check:\n1. Make sure your label template is valid\n2. Try restarting DYMO Connect\n3. Test printing from DYMO Connect app first`);
            }
            
            throw new Error(`Print failed: ${errorText}\n\nTroubleshooting steps:\n1. Power cycle your printer\n2. Check printer connection\n3. Try printing from DYMO Connect app first\n4. Restart DYMO Connect service`);
        }

        const printResult = await printResponse.text();
        console.log('Print result:', printResult);

        if (printResult.trim() === 'true') {
            this.showStatus(`Label printed successfully! (${labelType} - ${sku})`, 'success');
            
            // Clear the SKU field for next use
            document.getElementById('sku').value = '';
        } else {
            throw new Error(`Print failed: Unexpected response: ${printResult}`);
        }
        
        return printResult;
    }

    showStatus(message, type) {
        console.log('Status:', type, message);
        const statusElement = document.getElementById('status');
        statusElement.textContent = message;
        statusElement.className = `status ${type}`;
        statusElement.style.display = 'block';
        
        // Hide status after 5 seconds for success messages
        if (type === 'success') {
            setTimeout(() => {
                statusElement.style.display = 'none';
            }, 5000);
        }
    }
}

// Initialize the extension when the popup opens
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing DYMO Label Printer');
    new DymoLabelPrinter();
}); 