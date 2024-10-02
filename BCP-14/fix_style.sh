#!/bin/bash

sed -i -e 's/.yellow-background{background:#fafa00}/.yellow-background{background:#fafa00}\n.BCP{background:#bcbcbc; border-bottom: 2px solid #000000}\n.EBCP{background:#bebebe; border-bottom:2px dashed #000000}/' -e 's/class="aqua-background"/class="BCP"/g' -e 's/class="lime-background"/class="EBCP"/g' ./conventions_build/cf-conventions.html