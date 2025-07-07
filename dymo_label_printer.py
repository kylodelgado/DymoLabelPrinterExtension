#!/usr/bin/env python3
"""
DYMO Label Printer - Desktop App
A Python application that can stay on top and print DYMO labels
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import urllib.parse
import urllib.request
import ssl
import sys
import time

class DymoLabelPrinter:
    def __init__(self, root):
        self.root = root
        self.root.title("DYMO Label Printer")
        self.root.geometry("350x400")
        
        # Set window icon (optional)
        try:
            # You can add an icon file later
            pass
        except:
            pass
        
        # Load saved data
        self.config_file = os.path.expanduser("~/.dymo_label_printer.json")
        self.load_config()
        
        # Create SSL context that ignores certificate verification (for localhost)
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
        # Create GUI
        self.create_widgets()
        
        # Load saved label types
        self.update_label_dropdown()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.label_types = config.get('label_types', ['CPU', 'MOBO', 'SCREEN'])
                    self.always_on_top = config.get('always_on_top', False)
            else:
                self.label_types = ['CPU', 'MOBO', 'SCREEN']
                self.always_on_top = False
        except:
            self.label_types = ['CPU', 'MOBO', 'SCREEN']
            self.always_on_top = False
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                'label_types': self.label_types,
                'always_on_top': self.always_on_top
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def create_widgets(self):
        """Create the GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="DYMO Label Printer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Always on top checkbox
        self.on_top_var = tk.BooleanVar(value=self.always_on_top)
        self.on_top_checkbox = ttk.Checkbutton(
            main_frame, 
            text="Always stay on top", 
            variable=self.on_top_var,
            command=self.toggle_always_on_top
        )
        self.on_top_checkbox.grid(row=1, column=0, columnspan=2, pady=(0, 15), sticky=tk.W)
        
        # Label type section
        label_type_label = ttk.Label(main_frame, text="Label Type:")
        label_type_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        self.label_type_var = tk.StringVar()
        self.label_type_combo = ttk.Combobox(
            main_frame, 
            textvariable=self.label_type_var,
            state="readonly",
            width=30
        )
        self.label_type_combo.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Add new label type button (initially visible)
        self.add_label_button = ttk.Button(
            main_frame, 
            text="+ Add New Label Type", 
            command=self.show_add_label_section
        )
        self.add_label_button.grid(row=4, column=0, columnspan=2, pady=(0, 15))
        
        # Add new label type section (initially hidden)
        self.add_label_frame = ttk.Frame(main_frame)
        self.add_label_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(self.add_label_frame, text="Add new label type:").grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        self.new_label_var = tk.StringVar()
        self.new_label_entry = ttk.Entry(self.add_label_frame, textvariable=self.new_label_var, width=20)
        self.new_label_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        add_confirm_button = ttk.Button(self.add_label_frame, text="Add", command=self.add_label_type)
        add_confirm_button.grid(row=1, column=1, padx=(0, 5))
        
        cancel_button = ttk.Button(self.add_label_frame, text="Cancel", command=self.hide_add_label_section)
        cancel_button.grid(row=1, column=2)
        
        # Configure grid weights
        self.add_label_frame.columnconfigure(0, weight=1)
        
        # Hide the add label section initially
        self.add_label_frame.grid_remove()
        
        # SKU section
        sku_label = ttk.Label(main_frame, text="SKU:")
        sku_label.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        self.sku_var = tk.StringVar()
        self.sku_entry = ttk.Entry(main_frame, textvariable=self.sku_var, width=35)
        self.sku_entry.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Quantity section
        quantity_frame = ttk.Frame(main_frame)
        quantity_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        quantity_label = ttk.Label(quantity_frame, text="Quantity:")
        quantity_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_spinbox = ttk.Spinbox(
            quantity_frame, 
            from_=1, 
            to=99, 
            width=5, 
            textvariable=self.quantity_var,
            validate='key',
            validatecommand=(self.root.register(self.validate_quantity), '%P')
        )
        self.quantity_spinbox.grid(row=0, column=1, sticky=tk.W)
        
        quantity_info_label = ttk.Label(quantity_frame, text="(number of labels to print)", font=("Arial", 9))
        quantity_info_label.grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        
        # Configure quantity frame
        quantity_frame.columnconfigure(2, weight=1)
        
        # Print button
        self.print_button = ttk.Button(
            main_frame, 
            text="Print Label", 
            command=self.print_label,
            style="Accent.TButton"
        )
        self.print_button.grid(row=9, column=0, columnspan=2, pady=(0, 15))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            main_frame, 
            textvariable=self.status_var,
            font=("Arial", 10)
        )
        self.status_label.grid(row=10, column=0, columnspan=2, pady=(0, 10))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Bind Enter key events
        self.new_label_entry.bind('<Return>', lambda e: self.add_label_type())
        self.sku_entry.bind('<Return>', lambda e: self.print_label())
        
        # Bind quantity change to update button text
        self.quantity_var.trace_add('write', lambda *args: self.update_print_button_text())
        
        # Apply always on top if enabled
        if self.always_on_top:
            self.root.wm_attributes('-topmost', True)
    
    def show_add_label_section(self):
        """Show the add new label type section"""
        self.add_label_frame.grid()
        self.add_label_button.grid_remove()
        self.new_label_entry.focus()
    
    def hide_add_label_section(self):
        """Hide the add new label type section"""
        self.add_label_frame.grid_remove()
        self.add_label_button.grid()
        self.new_label_var.set("")
    
    def validate_quantity(self, value):
        """Validate quantity input - only allow positive integers"""
        if value == "":
            return True
        try:
            num = int(value)
            return 1 <= num <= 99
        except ValueError:
            return False
    
    def update_print_button_text(self):
        """Update print button text based on quantity"""
        try:
            quantity = int(self.quantity_var.get())
            if quantity == 1:
                self.print_button.config(text="Print Label")
            else:
                self.print_button.config(text=f"Print {quantity} Labels")
        except ValueError:
            self.print_button.config(text="Print Label")
    
    def toggle_always_on_top(self):
        """Toggle always on top setting"""
        self.always_on_top = self.on_top_var.get()
        self.root.wm_attributes('-topmost', self.always_on_top)
        self.save_config()
        
        if self.always_on_top:
            self.show_status("Window will stay on top", "success")
        else:
            self.show_status("Window will not stay on top", "info")
    
    def update_label_dropdown(self):
        """Update the label type dropdown with current values"""
        self.label_type_combo['values'] = self.label_types
        if self.label_types and not self.label_type_var.get():
            self.label_type_var.set(self.label_types[0])
    
    def add_label_type(self):
        """Add a new label type"""
        new_type = self.new_label_var.get().strip().upper()
        
        if not new_type:
            self.show_status("Please enter a label type", "error")
            return
        
        if new_type in self.label_types:
            self.show_status("Label type already exists", "error")
            return
        
        self.label_types.append(new_type)
        self.update_label_dropdown()
        self.label_type_var.set(new_type)
        self.save_config()
        self.show_status(f"Added label type: {new_type}", "success")
        self.hide_add_label_section()
    
    def print_label(self):
        """Print the label"""
        label_type = self.label_type_var.get()
        sku = self.sku_var.get().strip()
        
        if not label_type:
            self.show_status("Please select a label type", "error")
            return
        
        if not sku:
            self.show_status("Please enter a SKU", "error")
            return
        
        # Get quantity
        try:
            quantity = int(self.quantity_var.get())
            if quantity < 1 or quantity > 99:
                self.show_status("Please enter a quantity between 1 and 99", "error")
                return
        except ValueError:
            self.show_status("Please enter a valid quantity", "error")
            return
        
        try:
            self.show_status("Connecting to DYMO Connect...", "info")
            self.root.update()
            
            # Check DYMO Connect status
            if not self.check_dymo_connect():
                self.show_status("DYMO Connect is not running", "error")
                return
            
            # Print multiple labels
            successful_prints = 0
            total_prints = quantity
            
            for i in range(quantity):
                if quantity > 1:
                    self.show_status(f"Printing label {i + 1} of {quantity}...", "info")
                else:
                    self.show_status("Printing label...", "info")
                self.root.update()
                
                success, error_msg = self.send_print_request(label_type, sku)
                if success:
                    successful_prints += 1
                else:
                    self.show_status(f"Print {i + 1} failed: {error_msg}", "error")
                    break
                
                # Small delay between prints if printing multiple
                if quantity > 1 and i < quantity - 1:
                    time.sleep(0.5)  # 500ms delay between prints
            
            # Show final status
            if successful_prints == total_prints:
                if quantity == 1:
                    self.show_status(f"Label printed successfully! ({label_type} - {sku})", "success")
                else:
                    self.show_status(f"{successful_prints} labels printed successfully! ({label_type} - {sku})", "success")
                
                # Clear fields and reset quantity
                self.sku_var.set("")
                self.quantity_var.set("1")
            else:
                self.show_status(f"Only {successful_prints} of {total_prints} labels printed successfully", "error")
                
        except Exception as e:
            self.show_status(f"Error: {str(e)}", "error")
    
    def check_dymo_connect(self):
        """Check if DYMO Connect is running"""
        try:
            url = "https://127.0.0.1:41951/DYMO/DLS/Printing/StatusConnected"
            request = urllib.request.Request(url)
            
            with urllib.request.urlopen(request, context=self.ssl_context, timeout=5) as response:
                result = response.read().decode('utf-8').strip()
                print(f"DYMO Connect status check: {result}")
                return result == 'true'
                
        except Exception as e:
            print(f"DYMO Connect check failed: {e}")
            return False
    
    def send_print_request(self, label_type, sku):
        """Send print request to DYMO Connect"""
        try:
            # Create label XML
            label_xml = self.create_label_xml(label_type, sku)
            print(f"Created label XML (first 200 chars): {label_xml[:200]}...")
            
            # Manually encode form data like the working Chrome extension
            form_data_parts = [
                f"printerName={urllib.parse.quote('')}",
                f"printParamsXml={urllib.parse.quote('')}",
                f"labelXml={urllib.parse.quote(label_xml)}",
                f"labelSetXml={urllib.parse.quote('')}"
            ]
            form_data_string = '&'.join(form_data_parts)
            encoded_data = form_data_string.encode('utf-8')
            
            print(f"Form data length: {len(encoded_data)}")
            
            # Create request
            url = "https://127.0.0.1:41951/DYMO/DLS/Printing/PrintLabel"
            request = urllib.request.Request(
                url,
                data=encoded_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            print("Sending print request...")
            
            # Send request
            with urllib.request.urlopen(request, context=self.ssl_context, timeout=10) as response:
                result = response.read().decode('utf-8').strip()
                print(f"Print response: {result}")
                
                if result == 'true':
                    return True, ""
                else:
                    return False, f"Unexpected response: {result}"
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else str(e)
            print(f"HTTP Error {e.code}: {error_body}")
            
            if "Invalid parameter in stream" in error_body:
                return False, "XML formatting error - check DYMO Connect"
            elif e.code == 500:
                return False, "DYMO Connect internal error"
            else:
                return False, f"HTTP {e.code}: {e.reason}"
                
        except urllib.error.URLError as e:
            print(f"URL Error: {e}")
            return False, "Cannot connect to DYMO Connect"
            
        except Exception as e:
            print(f"Print request failed: {e}")
            return False, str(e)
    
    def create_label_xml(self, label_type, sku):
        """Create the label XML with placeholders replaced"""
        label_xml = '''<?xml version="1.0" encoding="utf-8"?>
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
      <Text>''' + sku + '''</Text>
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
          <String>''' + label_type + '''</String>
          <Attributes>
            <Font Family="Arial" Size="12" Bold="False" Italic="False" Underline="False" Strikeout="False"/>
            <ForeColor Alpha="255" Red="0" Green="0" Blue="0"/>
          </Attributes>
        </Element>
      </StyledText>
    </TextObject>
    <Bounds X="331" Y="163" Width="4442" Height="341.5669"/>
  </ObjectInfo>
</DieCutLabel>'''
        return label_xml
    
    def show_status(self, message, status_type="info"):
        """Show status message"""
        self.status_var.set(message)
        
        # Color coding for different status types
        if status_type == "error":
            self.status_label.configure(foreground="red")
        elif status_type == "success":
            self.status_label.configure(foreground="green")
        else:
            self.status_label.configure(foreground="black")
        
        self.root.update()
        
        # Clear success/info messages after 5 seconds
        if status_type in ["success", "info"]:
            self.root.after(5000, lambda: self.status_var.set("Ready"))
            self.root.after(5000, lambda: self.status_label.configure(foreground="black"))
    
    def on_closing(self):
        """Handle window closing"""
        self.save_config()
        self.root.destroy()

def main():
    """Main function"""
    root = tk.Tk()
    app = DymoLabelPrinter(root)
    root.mainloop()

if __name__ == "__main__":
    main() 